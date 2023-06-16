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
        self._server: BlockingOSCUDPServer | None = None
        self._message_queue = message_queue

    def start(self):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.message_handler)

        self._server = BlockingOSCUDPServer(
            ("127.0.0.1", self.receive_port),
            dispatcher,
        )

        thread = Thread(target=self._server.serve_forever)
        thread.start()

    def pause(self):
        if self._server:
            self._server.shutdown()

    def message_handler(self, address: str, args: list[Any]):
        """
        受信したOSC messageをQueueに追加する
        """
        osc_message = OSCMessage(address, args)
        self._message_queue.put(osc_message)
