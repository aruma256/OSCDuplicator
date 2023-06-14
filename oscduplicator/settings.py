import json
from pathlib import Path
from dataclasses import asdict

from oscduplicator.transmit_port_setting import TransmitPortSetting


class Settings:
    """
    OscDuplicatorの設定を保持するクラス

    Attributes
    ---------
    receive_port: int
        OSCReceiverのポート
    transmit_port_settings: list[TransmitPortSetting]
        OSCTransmitterのための設定
    """

    FILE_PATH = Path("./oscduplicator/settings.json")

    def __init__(self) -> None:
        self.receive_port, self.transmit_port_settings = self.load_json()

    def load_json(self):
        """
        jsonファイルからセーブデータを取得する
        """
        with Settings.FILE_PATH.open("r", encoding="UTF-8") as f:
            json_save = json.load(f)

        receive_port = json_save["receive"]["port"]
        transmit_port_settings = [
            TransmitPortSetting(**i) for i in json_save["transmit"]
        ]

        return receive_port, transmit_port_settings

    def save_json(self):
        """
        jsonファイルに設定を保存する
        """
        l_dict: list[dict] = [asdict(d) for d in self.transmit_port_settings]

        save_data: dict = {
            "receive": {"port": self.receive_port},
            "transmit": l_dict,
        }

        with Settings.FILE_PATH.open("w", encoding="UTF-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)

    def get_transmit_ports(self) -> list[int]:
        """
        OSCTransmitter用に転送先のポート番号のリストを取得する
        """
        return [setting.port for setting in self.transmit_port_settings]

    def update_receive_port_setting(self, port: int):
        self.receive_port = port

    def update_transmit_port_settings(
        self, transmit_port_settings: list[TransmitPortSetting]
    ):
        self.transmit_port_settings = transmit_port_settings

    def remove_transmit_port_setting(self, port: int):
        for i in range(len(self.transmit_port_settings)):
            if self.transmit_port_settings[i][0] == port:
                del self.transmit_port_settings[i]
                return

    def enable_transmit_port(self, port: int):
        for i in range(len(self.transmit_port_settings)):
            if self.transmit_port_settings[i][0] == port:
                self.transmit_port_settings[i][2] = True

    def disable_transmit_port(self, port: int):
        for i in range(len(self.transmit_port_settings)):
            if self.transmit_port_settings[i][0] == port:
                self.transmit_port_settings[i][2] = False
