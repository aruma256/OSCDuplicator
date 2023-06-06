import flet as ft
from typing import Callable

from duplicator import Duplicator


class ReceiverContainer(ft.UserControl):
    def __init__(
        self,
        duplicator: Duplicator,
        start_duplicate: Callable,
        stop_duplicate: Callable,
    ):
        super().__init__()
        self.duplicator = duplicator
        self.start_duplicate = start_duplicate
        self.stop_duplicate = stop_duplicate

    def build(self):
        self.receive_port = ft.Text(
            value=self.duplicator.settings.receive_port, size=20
        )

        self.edit_button = ft.ElevatedButton(
            text="編集",
        )

        return ft.Container(
            width=600,
            height=80,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            content=ft.Column(
                controls=[
                    ft.Text(value="受信", size=16),
                    ft.Row([self.receive_port, self.edit_button]),
                ]
            ),
        )

    def on_button_clicked(self):
        pass
