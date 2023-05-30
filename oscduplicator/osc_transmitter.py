from threading import Thread
from queue import Queue
import socket

from pythonosc.udp_client import SimpleUDPClient

from oscduplicator.osc_receiver import OSCMessage


class OSCTransmitter:
    """
    QueueからOSC messageを取り出し、各ポートへ転送する

    Attributes
    ---------
    transmit_ports: list[int]
        OSC信号を再送信するための、portのリスト
    clients: list[SimpleUDPClient]
        OSC信号を再送信するための、clientのリスト
    q: Queue
        OSC信号の受信順・送信順を保証するためのキュー
    is_shutdown: bool
        transmitterを停止するためのフラグ

    """

    def __init__(self, q: Queue) -> None:
        self.transmit_ports: list[int] = []
        self.__q: Queue = q
        self.clients: list[SimpleUDPClient] = self.init_clients(
            self.transmit_ports
        )
        self.is_shutdown = False

    def init_clients(self, transmit_ports):
        """
        OSCクライエントを初期化
        """

        def __client(port: int) -> SimpleUDPClient:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            str_ip = str(ip)
            return SimpleUDPClient(str_ip, port)

        return [__client(i) for i in transmit_ports]

    def start_transmitter(self):
        """
        OSCTransmitterを起動
        """
        th = Thread(target=self.transmit_forever)
        th.start()

    def transmit_forever(self):
        self.is_shutdown = False

        while not self.is_shutdown:
            self.transmit_message(self.__q, self.clients)

    def transmit_message(self, q: Queue, clients: list[SimpleUDPClient]):
        if not clients:
            osc_message: OSCMessage = q.get()

            for client in clients:
                client.send_message(osc_message.address, osc_message.message)

            q.task_done()

    def stop_transmitter(self):
        self.is_shutdown = True
