import flet as ft

from oscduplicator.duplicator import Duplicator

from oscduplicator.gui.header import Header
from oscduplicator.gui.receiver_container import ReceiverContainer
from oscduplicator.gui.transmitter_container import TransmitterContainer
from oscduplicator.gui.option_setting_container import OptionSettingContainer

APP_TITLE = "OSCDuplicator"


class App:
    def main(self, page: ft.Page):
        page.title = APP_TITLE
        page.horizontal_alignment = "center"
        page.window_width, page.window_height = 600, 800

        self.duplicator = Duplicator()
        self.duplicator.load_settings()

        self.header = Header(self.duplicator)
        self.option_setting_container = OptionSettingContainer(self.duplicator)
        self.receiver_container = ReceiverContainer(self.duplicator)  # ポートは仮
        self.transmitter_container = TransmitterContainer(self.duplicator)

        page.add(self.header)
        page.add(self.option_setting_container)
        page.add(self.receiver_container)
        page.add(self.transmitter_container)


def start():
    ft.app(target=App().main)


if __name__ == "__main__":
    start()
