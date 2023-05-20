import json
import queue
from dataclasses import dataclass
from threading import Thread
from typing import Optional

from pythonosc import dispatcher, osc_server, udp_client


@dataclass
class TransmitPortSetting:
    """
    再送信先のポートのデータを保持する

    Parameters
    ---------
    name: str
        ポートの名称
    port: int
        ポート番号
    enable: bool
        そのポートに再送信するかどうか
    """

    name: str
    port: int
    enabled: bool

    def __post_init__(self):
        # Validate the 'name' attribute
        if not isinstance(self.name, str):
            raise TypeError(
                "Expected instance of type 'str' for attribute 'name',"
                f"but got '{type(self.name).__name__}'."
            )

        # Validate the 'port' attribute
        if not isinstance(self.port, int):
            raise TypeError(
                "Expected instance of type 'int' for attribute 'port',"
                f" but got '{type(self.port).__name__}'."
            )
        if not (0 <= self.port <= 65535):  # standard port range for TCP/UDP
            raise ValueError(
                "Invalid 'port' value. Expected a number between 0 and 65535, "
                f"but got '{self.port}'."
            )

        # Validate the 'enabled' attribute
        if not isinstance(self.enabled, bool):
            raise TypeError(
                "Expected instance of type 'bool' for attribute 'enabled',"
                f" but got '{type(self.enabled).__name__}'."
            )


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
        self.__receive_port: Optional[int] = None
        self.__transmit_port_settings: list[TransmitPortSetting] = []
        self.__server: Optional[osc_server.ThreadingOSCUDPServer] = None
        self.__clients: list[udp_client.SimpleUDPClient] = []
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
            raise TypeError("Expected instance of type 'int' for attribute 'port'")
        if not (0 <= value <= 65535):  # standard port range for TCP/UDP
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

        self.__server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", port), dpt)
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
        self, transmit_clients: list[udp_client.SimpleUDPClient], q: queue.Queue
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

        if len(transmit_clients) <= 0:
            return

        while True:
            d = q.get()
            address: str = d["address"]
            args: list = d["args"]

            threads = [
                Thread(target=client.send_message, args=(address, args))
                for client in transmit_clients
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            q.task_done()

    def load_settings(self, file_path: str):
        self.receive_port, self.transmit_list = self.__load_json(file_path)

    def __load_json(self, file_path: str):
        """
        jsonファイルから設定データを呼び出し

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

        receive_port = json_dic["receive"]

        transmit_list: list[TransmitPortSetting] = [
            TransmitPortSetting(**i) for i in json_dic["transmit"]
        ]

        return receive_port, transmit_list
