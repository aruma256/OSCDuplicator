from pathlib import Path
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

    FILE_PATH = Path("./oscduplicator/settings.json")

    def __init__(self) -> None:
        self.settings = Settings(Duplicator.FILE_PATH)
        self.queue = Queue()
        self.receiver: OSCReceiver | None = None
        self.transmitter = OSCTransmitter(self.queue)
        self.is_duplicate = False

    def start_duplicate(self, receive_port, transmit_port_settings):
        """
        On start button pushed

        Attribute
        ---------
        receive_port: int
            OSCReceiverのポート
        transmit_port_settings: list[TransmitPortSettings]
            OSCTransmitterのための設定
        """
        self.__update_settings(receive_port, transmit_port_settings)

        self.receiver = OSCReceiver(self.settings.receive_port, self.queue)

        self.transmitter.transmit_ports = self.settings.get_transmit_ports()
        self.transmitter.create_clients(self.transmitter.transmit_ports)

        self.receiver.start()
        self.transmitter.start()

        self.is_duplicate = True

    def stop_duplicate(self):
        """
        On stop button pushed
        """
        if self.receiver:
            self.receiver.stop()

        self.transmitter.stop()

        self.is_duplicate = False

    def __update_settings(self, receive_port, transmit_port_settings):
        """
        Parameters
        ---------
        receive_port: int
            OSCReceiverのポート
        transmit_port_settings: list[TransmitPortSettings]
            OSCTransmitterのための設定
        """
        self.settings.update_receive_port_setting(receive_port)
        self.settings.update_transmit_port_settings(transmit_port_settings)

    def save_settings(self):
        self.settings.save_json(Duplicator.FILE_PATH)
