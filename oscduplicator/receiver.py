from dataclasses import dataclass
from threading import Thread
from typing import Any
from queue import Queue

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


@dataclass(frozen=True)
class OSCMessage:
    address: str
    message: list[Any]


class OSCReceiver:
    """
    OSC messageを受信し、Queueに追加する

    Attributes
    ---------
    receive_port: int
        OSC信号を受信するためのポート番号
    server: BlockingOSCUDPServer
        OSC信号を受信するためのサーバー
    q: Queue
        受信したOSC messageを格納するキュー
    """

    def __init__(self, receive_port: int) -> None:
        self.receive_port: int = receive_port
        self.server: BlockingOSCUDPServer = self.init_server()
        self.q = Queue()

    def init_server(self):
        """
        OSCサーバーを初期化
        """
        dpt = Dispatcher()
        dpt.map("*", self.q_put)

        return BlockingOSCUDPServer(("0, 0, 0, 0", self.receive_port), dpt)

    def start_receiver(self):
        """
        OSCReceiverを起動する
        """
        th = Thread(target=self.server.serve_forever)
        th.start()

    def stop_receiver(self):
        """
        OSCReceiverを終了する
        """
        self.server.shutdown()

    def q_put(self, address: str, *args: list[Any]):
        """
        受信したOSC messageとaddressをQueueに追加する
        """
        osc_message = OSCMessage(address, *args)
        self.q.put(osc_message)
