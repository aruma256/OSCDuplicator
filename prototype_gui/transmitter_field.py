import flet as ft
from flet import (
    Checkbox,
    UserControl,
    TextField,
    Row,
)

from duplicator import Duplicator


class TransmitterField(UserControl):
    """
    転送ポートの設定を記録、表示

    Attribute
    ---------
    """

    def __init__(self, duplicator: Duplicator, index=0, empty=False):
        super().__init__()
        self.duplicator = duplicator
        self.index = index

        if empty:
            name = ""
            port = None
            enabled = False
        else:
            port = self.duplicator.settings.transmit_port_settings[index].port
            name = self.duplicator.settings.transmit_port_settings[index].name
            enabled = self.duplicator.settings.transmit_port_settings[
                index
            ].enabled

        self.name: TextField = self.__init_tb_name(name)
        self.port: TextField = self.__init_tb_port(port)
        self.enabled: Checkbox = self.__init_checkbox_enable(enabled)

    def build(self):
        return Row([self.port, self.name, self.enabled])

    def __init_tb_name(self, name):
        return TextField(
            value=name, disabled=False, on_blur=self.on_name_blur, width=300
        )

    def __init_tb_port(self, port: None | int):
        return TextField(
            value=port,
            disabled=False,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_blur=self.on_port_blur,
            width=200,
            counter_style=ft.TextStyle(color=ft.colors.RED),
        )

    def __init_checkbox_enable(self, enabled: bool):
        return Checkbox(
            value=enabled, disabled=False, on_change=self.on_checkbox_change
        )

    def on_name_blur(self, e):
        self.duplicator.settings.transmit_port_settings[
            self.index
        ].name = self.name.value

    def on_port_blur(self, e):
        try:
            self.validate_port(self.port.value)
        except (TypeError, ValueError) as e:
            self.port.counter_text = "0-65535"
            self.duplicator.settings.transmit_port_settings[
                self.index
            ].port = None
        else:
            self.port.counter_text = None
            self.duplicator.settings.transmit_port_settings[
                self.index
            ].port = self.port.value

    def on_checkbox_change(self, e):
        self.duplicator.settings.transmit_port_settings[
            self.index
        ].enabled = self.enabled.value

    @staticmethod
    def validate_port(port: int) -> None:
        """
        ポート番号の型・値を確認
        """
        if not isinstance(port, int):
            raise TypeError()
        if not (0 <= port <= 65535):
            raise ValueError()
