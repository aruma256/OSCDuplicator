from dataclasses import dataclass
from threading import Thread
from typing import Any
from queue import Queue

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


@dataclass(frozen=True)
class OSCMessage:
    address: str
    message: tuple[Any]


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

    def __init__(self, message_queue: Queue) -> None:
        self._receive_port: int | None = None
        self._server: BlockingOSCUDPServer | None = None
        self._message_queue = message_queue

    def start(self):
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.message_handler)

        self._server = BlockingOSCUDPServer(
            ("127.0.0.1", self._receive_port),
            dispatcher,
        )

        thread = Thread(target=self._server.serve_forever)
        thread.start()

    def pause(self):
        if self._server:
            self._server.shutdown()

    def update_receive_port(self, receive_port: int):
        self._receive_port = receive_port
        if self._server:
            self.pause()
            self.start()

    def message_handler(self, address: str, *args: Any):
        """
        受信したOSC messageをQueueに追加する
        """
        osc_message = OSCMessage(address, args)
        self._message_queue.put(osc_message)
