import json
import queue
import socket
from dataclasses import asdict
from threading import Thread

from pythonosc import dispatcher, osc_server, udp_client
from oscduplicator.setting import TransmitPortSetting


class OSCDuplicator:
    """
    OSC信号を受信するためのサーバーと、再送信のための設定を保持する

    Attributes
    ---------
    server: osc_server.ThreadingOSCUDPServer
        OSC信号を受信するためのサーバー
    receive_port: int
        OSC信号を受信するためのポート、デフォルト9001
    transmit_port_settings: list[TransmitPortSetting]
        転送先ポートの設定を保持するリスト
    clients: list[udp_client.SimpleUDPClient]
        OSC信号を再送信するための、clientのリスト
    q: queue.Queue
        OSC信号の受信順・送信順を保証するためのキュー
    """

    def __init__(self) -> None:
        self.__receive_port: int | None = None
        self.__transmit_port_settings: list[TransmitPortSetting] = []
        self.__server: osc_server.ThreadingOSCUDPServer | None = None
        self.clients: list[udp_client.SimpleUDPClient] = []
        self.__q = queue.Queue()

    @property
    def receive_port(self):
        return self.__receive_port

    @receive_port.setter
    def receive_port(self, value: int):
        """
        __receiver_portのsetter
        値のチェックをする

        Parameters
        ---------
        value: int
            新しい受信ポート番号
        """
        # check value
        if not isinstance(value, int):
            raise TypeError(
                "Expected instance of type 'int' for attribute 'port'"
            )
        if not (0 <= value <= 65535):
            raise ValueError(
                "Invalid 'port' value. Expected a number between 0 and 65535"
            )
        self.__receive_port = value

    def start_server(self) -> None:
        """
        OSCサーバーを初期化し、起動する
        """
        port = self.receive_port if self.receive_port is not None else 9001
        dpt = dispatcher.Dispatcher()

        dpt.map("/*", self.__queue_osc)

        self.__server = osc_server.ThreadingOSCUDPServer(
            ("127.0.0.1", port), dpt
        )
        self.__server.serve_forever()

    def stop_server(self) -> None:
        """
        OSCサーバーを終了する
        """
        self.__server.shutdown()

    def __queue_osc(self, q: queue.Queue, address: str, *args: list) -> None:
        """
        受信したOSC信号をdictとして、キューに追加する

        Parameters
        ---------
        address: str
            受信・再送信アドレス
        args: list
            osc信号
        """
        d = {"address": address, "args": args}
        q.put(d)

    def transmit_msg(
        self, clients: list[udp_client.SimpleUDPClient], q: queue.Queue
    ) -> None:
        """
        osc信号を転送する

        Parameters
        ---------
        transmit_clients: list[udp_client.SimpleUDPClient]
            OSC信号を再送信するための、clientのリスト
        q: queue.Queue
            キュー
            {"address": address, "args": args}
        """

        if len(clients) <= 0:
            return

        while True:
            d = q.get()
            address: str = d["address"]
            args: list = d["args"]

            threads = [
                Thread(target=client.send_message, args=(address, args))
                for client in clients
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            q.task_done()

    def load_settings(self, file_path: str) -> None:
        """
        jsonファイルを読み込み、
        self.__transmit_port_settingsと
        self.clients
        を更新する
        起動時に呼び出される

        Parameters
        ---------
        file_path: str
            設定ファイルのパス
        """
        self.receive_port, self.__transmit_port_settings = self.__load_json(
            file_path
        )
        self.__update_clients(self.__transmit_port_settings)

    def __load_json(self, file_path: str):
        """
        jsonファイルから設定データを呼び出す

        Parameters
        ---------
        file_path: str
            設定ファイルのパス

        Returns
        ---------
        receive_port: int
            受信ポート
        transmit_list: list[TransmitPortSettings]
            分配ポートのセッティング(dataclass)のリスト
        """

        with open(file_path, "r", encoding="UTF-8") as f:
            json_dic = json.load(f)

        receive_port = json_dic["receive"]["port"]

        transmit_port_settings: list[TransmitPortSetting] = [
            TransmitPortSetting(**i) for i in json_dic["transmit"]
        ]

        return receive_port, transmit_port_settings

    def __update_clients(
        self, transmit_port_settings: list[TransmitPortSetting]
    ) -> None:
        """
        self.__clientsを更新する
        load_settings()と
        update_settings()で呼び出される

        Parameters
        """

        def __client(port: int) -> udp_client.SimpleUDPClient:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            str_ip = str(ip)
            return udp_client.SimpleUDPClient(str_ip, port)
        
        port_l: list[int] = []
        for tps in transmit_port_settings:
            if tps.enabled:
                port_l.append(tps.port)

        port_l = list(set(port_l))

        self.clients = [__client(i) for i in port_l]

    def update_settings(
        self,
        receive_port: int,
        transmit_port_settings: list[TransmitPortSetting],
    ) -> None:
        """
        GUIでの入力内容から、
        self.receive_portと
        self.__transmit_port_settingsと
        self.clients を更新する
        OSCDuplicator内のstart_server()の前とsave_settings()の前に呼び出す

        Parameters
        ---------
        receive_port: int
        transmit_port_settings: list[TransmitPortSetting]
            app側では入力内容からlist[TransmitPortSetting]を作成して引数として設定する
            なんか二度手間なような気がする
        """
        self.receive_port = receive_port
        self.__transmit_port_settings = transmit_port_settings
        self.__update_clients(self.__transmit_port_settings)

    def save_settings(self, file_path: str) -> None:
        """
        メンバ変数をjsonファイルにセーブする
        終了時に呼び出す
        """

        transmit_settings: list[dict] = [
            asdict(d) for d in self.__transmit_port_settings
        ]

        save_data: dict = {
            "receive": {"port": self.receive_port},
            "transmit": transmit_settings
        }

        with open(file_path, "w", encoding="UTF-8") as f:
            json.dump(save_data, f, indent=4)
