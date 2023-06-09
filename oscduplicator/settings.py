from dataclasses import asdict
import json
from pathlib import Path

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
    auto_start: bool
        起動時に自動で受信->転送するかの設定
    """

    FILE_PATH = Path("./settings.json")

    def __init__(self) -> None:
        self._receive_port: int = 9001
        self.transmit_port_settings: list[TransmitPortSetting] = []
        self.auto_start: bool = False

    @property
    def receive_port(self) -> int:
        return self._receive_port

    def load(self) -> None:
        if not Settings.FILE_PATH.exists():
            return

        with Settings.FILE_PATH.open("r", encoding="UTF-8") as f:
            data = json.load(f)

        self.transmit_port_settings.clear()
        self.update_receive_port_setting(data["receive"]["port"])
        for element in data["transmit"]:
            self.add_transmit_port_setting(
                name=element["name"],
                port=element["port"],
                enabled=element["enabled"],
            )
        self.auto_start = data["auto_start"]

    def save_json(self):
        save_data = {
            "receive": {"port": self.receive_port},
            "transmit": list(map(asdict, self.transmit_port_settings)),
            "auto_start": self.auto_start,
        }

        with Settings.FILE_PATH.open("w", encoding="UTF-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)

    def update_receive_port_setting(self, port: int) -> bool:
        if self.receive_port == port:
            return False
        if any(s.port == port for s in self.transmit_port_settings):
            return False
        self._receive_port = port
        return True

    def add_transmit_port_setting(self,
                                  name: str, port: int, enabled: bool) -> bool:
        if self.receive_port == port:
            return False
        if any(s.port == port for s in self.transmit_port_settings):
            return False
        self.transmit_port_settings.append(
            TransmitPortSetting(name, port, enabled)
        )
        return True

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
