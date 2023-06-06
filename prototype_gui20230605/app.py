import flet as ft

from duplicator import Duplicator
from header import Header
from receiver_container import ReceiverContainer
from transmitter_container import TransmitterContainer

APP_TITLE = "OSCDuplicator"


class App:
    def main(self, page: ft.Page):
        self.duplicator = Duplicator()

        page.title = APP_TITLE
        page.horizontal_alignment = "center"
        page.window_width, page.window_height = 600, 800

        self.header = Header(
            self.duplicator, self.start_duplicate, self.stop_duplicate
        )
        self.receiver_container = ReceiverContainer(
            self.duplicator, self.start_duplicate, self.stop_duplicate
        )
        self.transmitter_container = TransmitterContainer(
            self.duplicator, on_edit_clicked
        )

        page.add(self.header)
        page.add(self.receiver_container)
        page.add(self.transmitter_container)

    def start_duplicate(self):
        """
        全体スタート
        """
        self.duplicator.start_duplicate(
            self.duplicator.settings.receive_port,
            self.duplicator.settings.transmit_port_settings,
        )
        self.header.update_status_text()
        self.header.update_run_button()

    def stop_duplicate(self):
        """
        全体ストップ
        """
        self.duplicator.stop_duplicate()
        self.header.update_status_text()
        self.header.update_run_button()


def start():
    ft.app(target=App().main)


def on_edit_clicked():
    pass


if __name__ == "__main__":
    start()
