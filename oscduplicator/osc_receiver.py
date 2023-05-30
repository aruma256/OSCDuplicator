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
    _message_queue: Queue
        受信したOSC messageを格納するキュー
    """

    def __init__(self, receive_port: int, message_queue: Queue) -> None:
        self.receive_port: int = receive_port
        self.server: BlockingOSCUDPServer = self._create_server()
        self._message_queue = message_queue

    def _create_server(self):
        """
        OSCサーバーを作成する
        """
        dpt = Dispatcher()
        dpt.map("*", self.message_handler)

        return BlockingOSCUDPServer(("0, 0, 0, 0", self.receive_port), dpt)

    def start(self):
        """
        OSCReceiverを起動する
        """
        th = Thread(target=self.server.serve_forever)
        th.start()

    def stop(self):
        """
        OSCReceiverを終了する
        """
        self.server.shutdown()

    def message_handler(self, address: str, args: list[Any]):
        """
        受信したOSC messageとaddressをQueueに追加する
        """
        osc_message = OSCMessage(address, args)
        self._message_queue.put(osc_message)
