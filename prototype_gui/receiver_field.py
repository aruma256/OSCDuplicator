import flet as ft
from flet import UserControl, TextField

from duplicator import Duplicator


class ReceiverField(UserControl):
    """
    receive_portの入力欄

    Attributes
    ---------
    duplicator: Duplicator
        Appのバックエンド
    receive_port: Text
        受信ポート
    """

    def __init__(self, duplicator: Duplicator):
        super().__init__()
        self.duplicator = duplicator
        self.input_field = TextField(
            disabled=False,
            value=self.duplicator.settings.receive_port,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_blur=self.on_blur,
            width=200,
            counter_style=ft.TextStyle(color=ft.colors.RED),
        )

    def build(self):
        return self.input_field

    def on_blur(self, e):
        try:
            self.validate_port(self.input_field.value)
        except (TypeError, ValueError):
            self.input_field.counter_text = "0-65535"
        else:
            self.input_field.counter_text = None
            self.duplicator.settings.receive_port = self.input_field.value

    @staticmethod
    def validate_port(port: int) -> None:
        """
        ポート番号の型・値を確認
        """
        if not isinstance(port, int):
            raise TypeError()
        if not (0 <= port <= 65535):
            raise ValueError()
