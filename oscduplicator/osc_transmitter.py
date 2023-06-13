from threading import Thread, Lock
from queue import Queue

from pythonosc.udp_client import SimpleUDPClient

from oscduplicator.osc_receiver import OSCMessage
from oscduplicator.transmit_port_setting import TransmitPortSetting


class OSCTransmitter:
    ADDRESS = "127.0.0.1"

    def __init__(self, q: Queue[OSCMessage]) -> None:
        self._q = q
        self._clients: dict[int, SimpleUDPClient] = {}
        self._clients_lock = Lock()
        self._transmit_port_settings: list[TransmitPortSetting] = []
        self._thread = Thread(target=self._loop, daemon=True)
        self._thread.start()
        self._running = False

    def start(self) -> None:
        self._running = True

    def pause(self) -> None:
        self._running = False

    def update(self,
               transmit_port_settings: list[TransmitPortSetting]) -> None:
        with self._clients_lock:
            self._clients.clear()
            for setting in transmit_port_settings:
                self._clients[setting.port] = SimpleUDPClient(
                    OSCTransmitter.ADDRESS, setting.port
                )
            self._transmit_port_settings = transmit_port_settings

    def get_transmit_port_settings(self) -> list[TransmitPortSetting]:
        return self._transmit_port_settings

    def _loop(self) -> None:
        while True:
            message = self._q.get()
            if self._running:
                self._transmit(message)

    def _transmit(self, message: OSCMessage):
        for client in self._clients.values():
            client.send_message(message.address, message.message)
