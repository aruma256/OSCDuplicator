from pathlib import Path
from settings import Settings


class Duplicator:
    """
    Duplicatorのダミー

    Attribute
    ---------
    is_duplicate: bool
    """

    FILE_PATH = Path(".\prototype_gui\settings.json")

    def __init__(self) -> None:
        self.settings = Settings(Duplicator.FILE_PATH)
        self.is_duplicate = False

    def start_duplicate(self, receive_port, transmit_port_settings):
        self.is_duplicate = True

    def stop_duplicate(self):
        self.is_duplicate = False

    def save_settings(self):
        self.settings.save_json(Duplicator.FILE_PATH)
