import flet as ft
from typing import Callable

from duplicator import Duplicator


class Header(ft.UserControl):
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
        self.text = ft.Text(
            value="Duplicator stopped", size=40, weight=ft.FontWeight.BOLD
        )

        self.button = ft.ElevatedButton(
            text="stop",
            bgcolor=ft.colors.LIGHT_GREEN_ACCENT_400,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            color=ft.colors.WHITE,
            on_click=self.on_button_clicked,
        )

        return ft.Container(
            width=600,
            height=80,
            content=ft.Row(
                [self.text, self.button],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=ft.colors.INDIGO_50,
            margin=0,
        )

    def on_button_clicked(self, _):
        if not self.duplicator.is_duplicate:
            self.start_duplicate()
        else:
            self.stop_duplicate()

        self.update()

    def update_status_text(self):
        """
        dupkicatorの実行状態に応じて、
        テキストを変更
        """
        if not self.duplicator.is_duplicate:
            self.text.value = "Duplicator stopped"
        else:
            self.text.value = "Duplicator started"

    def update_run_button(self):
        """
        dupkicatorの実行状態に応じて、
        ボタンのテキスト・レイアウトを変更
        """
        if not self.duplicator.is_duplicate:
            self.button.text = "start"
            self.button.bgcolor = ft.colors.LIGHT_GREEN_ACCENT_400

        else:
            self.button.text = "stop"
            self.button.bgcolor = ft.colors.RED
