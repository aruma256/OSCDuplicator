from pathlib import Path

from oscduplicator.receiver import OSCReceiver
from oscduplicator.settings import Settings
from oscduplicator.transmitter import OSCTransmitter


class Duplicator:
    """
    OSCDuplicatorのバックエンドを統括するクラス

    Attributes
    settings: Settings
        送信・受信に関する設定を保持するクラスのインスタンスオブジェクト
    receiver: OSCReceiver
        OSC messageを受信するクラスのインスタンスオブジェクト
    transmitter: OSCTransmitter
        OSC messageを各ポートへ転送するクラスのインスタンスオブジェクト
    """

    FILE_PATH = Path("./oscduplicator/settings.json")

    def __init__(self) -> None:
        self.settings = Settings(Duplicator.FILE_PATH)
        self.receiver = OSCReceiver(self.settings.receive_port)
        self.transmitter = OSCTransmitter(self.receiver.q)

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

        self.receiver.receive_port = self.settings.receive_port
        self.receiver.init_server()

        self.transmitter.transmit_ports = self.settings.get_transmit_ports()
        self.transmitter.init_clients(self.transmitter.transmit_ports)

        self.receiver.start_receiver()
        self.transmitter.start_transmitter()

    def stop_duplicate(self):
        """
        On stop button pushed
        """
        self.receiver.stop_receiver()
        self.transmitter.stop_transmitter()

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
