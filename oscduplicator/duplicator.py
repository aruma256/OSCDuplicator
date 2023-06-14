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
        self.receiver: OSCReceiver | None = None
        self.transmitter = OSCTransmitter(self.queue)
        self.is_duplicate = False

    def start_duplicate(self) -> None:
        """
        startボタンが押されたときに呼び出される
        """
        self.receiver = OSCReceiver(self.settings.receive_port, self.queue)

        self.transmitter.update_transmit_port(
            self.settings.get_transmit_ports()
        )

        self.receiver.start()
        self.transmitter.start()

        self.is_duplicate = True

    def stop_duplicate(self):
        """
        On stop button pushed
        """
        if self.receiver:
            self.receiver.stop()

        self.transmitter.pause()

        self.is_duplicate = False

    def save_settings(self):
        self.settings.save_json()
