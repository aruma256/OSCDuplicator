import flet as ft
from flet import Container, UserControl, ElevatedButton, Text, Row

from duplicator import Duplicator


class Header(UserControl):
    """
    Appのヘッダー
    duplicatorの実行状態, start/stop button

    Attribute
    ---------
    duplicator: Duplicator
        Appのバックエンド
    status_text: Text()
        duplicatorの実行状態
    run_button: ElevatedButton
        start/stopボタン
    """

    def __init__(self, duplicator: Duplicator):
        super().__init__()
        self.duolicator = duplicator
        self.status_text = self.init_status_text()
        self.run_button = self.init_run_button()

    def build(self):
        return Container(
            width=600,
            height=80,
            content=Row(
                [self.status_text, self.run_button],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=ft.colors.INDIGO_50,
            margin=0,
        )

    def init_status_text(self):
        """
        status_textの初期設定
        """
        return Text(
            value="Duplicator stopped", size=40, weight=ft.FontWeight.BOLD
        )

    def init_run_button(self):
        """
        run_buttonの初期設定
        """
        return ElevatedButton(
            text="stop",
            bgcolor=ft.colors.LIGHT_GREEN_ACCENT_400,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            color=ft.colors.WHITE,
            on_click=self.run_button_clicked,
        )

    def run_button_clicked(self, e):
        """
        run_buttonが押された場合の処理
        """
        if not self.duolicator.is_duplicate:
            self.duolicator.start_duplicate(
                self.duolicator.settings.receive_port,
                self.duolicator.settings.transmit_port_settings,
            )
        else:
            self.duolicator.stop_duplicate()

        self.__update_status_text()
        self.__update_run_button()

        self.update()

    def __update_status_text(self):
        """
        dupkicatorの実行状態に応じて、テキストを変更
        """
        if not self.duolicator.is_duplicate:
            self.status_text.value = "Duplicator stopped"
        else:
            self.status_text.value = "Duplicator started"

    def __update_run_button(self):
        """
        dupkicatorの実行状態に応じて、
        ボタンのテキスト・レイアウトを変更
        """
        if not self.duolicator.is_duplicate:
            self.run_button.text = "start"
            self.run_button.bgcolor = ft.colors.LIGHT_GREEN_ACCENT_400

        else:
            self.run_button.text = "stop"
            self.run_button.bgcolor = ft.colors.RED
