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
        self.receive_port: int | None = None
        self.transmit_port_settings: list[TransmitPortSetting] = []

    def load_json(self) -> None:
        """
        jsonファイルからセーブデータを取得する
        """
        with Settings.FILE_PATH.open("r", encoding="UTF-8") as f:
            data = json.load(f)

        self.receive_port = data["receive"]["port"]
        self.transmit_port_settings.clear()
        for element in data["transmit"]:
            self.transmit_port_settings.append(
                TransmitPortSetting(
                    name=element["name"],
                    port=element["port"],
                    enabled=element["enabled"],
                )
            )

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

    def update_receive_port_setting(self, port: int):
        self.receive_port = port

    def update_transmit_port_settings(
        self, transmit_port_settings: list[TransmitPortSetting]
    ):
        self.transmit_port_settings = transmit_port_settings

    def remove_transmit_port_setting(self, port: int) -> None:
        for i in reversed(range(len(self.transmit_port_settings))):
            if self.transmit_port_settings[i].port == port:
                del self.transmit_port_settings[i]

    def enable_transmit_port(self, port: int) -> None:
        for setting in self.transmit_port_settings:
            if setting.port == port:
                setting.enabled = True

    def disable_transmit_port(self, port: int) -> None:
        for setting in self.transmit_port_settings:
            if setting.port == port:
                setting.enabled = False
