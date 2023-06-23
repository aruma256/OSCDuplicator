from queue import Queue

from oscduplicator.osc_receiver import OSCReceiver
from oscduplicator.settings import Settings
from oscduplicator.osc_transmitter import OSCTransmitter


class Duplicator:
    """
    OSCDuplicatorのバックエンドを統括するクラス

    Attributes
    settings: Settings
        送信・受信に関する設定を保持するクラスのインスタンスオブジェクト
    queue: Queue
        受信したOSC messageの複製送信待ちキュー
    receiver: OSCReceiver
        OSC messageを受信するクラスのインスタンスオブジェクト
    transmitter: OSCTransmitter
        OSC messageを各ポートへ転送するクラスのインスタンスオブジェクト
    is_duplicate: bool
        dulicatorが実行されているかどうか
    """

    def __init__(self) -> None:
        self.settings = Settings()
        self.queue = Queue()
        self.receiver = OSCReceiver(self.queue)
        self.transmitter = OSCTransmitter(self.queue)
        self.is_duplicate = False

    def load_settings(self) -> None:
        self.settings.load_settings()
        self.receiver.update_receive_port(self.settings.receive_port)
        self.transmitter.update_transmit_port(
            self.settings.transmit_port_settings
        )

    def start_duplicate(self) -> None:
        """
        startボタンが押されたときに呼び出される
        """
        self.receiver.start()
        self.transmitter.start()

        self.is_duplicate = True

    def stop_duplicate(self):
        """
        On stop button pushed
        """
        self.receiver.pause()
        self.transmitter.pause()

        self.is_duplicate = False

    def save_settings(self):
        self.settings.save_json()

    def add_transmit_port(self, name: str, port: int):
        ret = self.settings.add_transmit_port_setting(name, port, False)
        if ret:
            self.transmitter.update_transmit_port(
                self.settings.transmit_port_settings
            )

    def remove_transmit_port(self, port: int):
        self.settings.remove_transmit_port_setting(port)
        self.transmitter.update_transmit_port(
            self.settings.transmit_port_settings
        )

    def update_receive_port(self, port: int):
        ret = self.settings.update_receive_port_setting(port)
        if ret:
            self.receiver.update_receive_port(self.settings.receive_port)
