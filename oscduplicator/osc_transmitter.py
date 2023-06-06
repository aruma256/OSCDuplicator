from threading import Thread, Lock
from queue import Queue

from pythonosc.udp_client import SimpleUDPClient

from oscduplicator.osc_receiver import OSCMessage


class OSCTransmitter:
    ADDRESS = "127.0.0.1"

    def __init__(self, q: Queue[OSCMessage]) -> None:
        self._q = q
        self._clients: dict[int, SimpleUDPClient] = {}
        self._clients_lock = Lock()
        self._thread = Thread(target=self._loop, daemon=True)
        self._thread.start()
        self._running = False

    def start(self) -> None:
        self._running = True

    def pause(self) -> None:
        self._running = False

    def _loop(self) -> None:
        while True:
            message = self._q.get()
            if self._running:
                self._transmit(message)

    def _transmit(self, message: OSCMessage):
        for client in self._clients.values():
            client.send_message(message.address, message.message)

    def add_destination_port(self, port: int) -> bool:
        with self._clients_lock:
            if port not in self._clients:
                self._clients[port] = SimpleUDPClient(OSCTransmitter.ADDRESS,
                                                      port)
                return True
            else:
                return False

    def remove_destination_port(self, port: int) -> None:
        with self._clients_lock:
            if port in self._clients:
                del self._clients[port]
