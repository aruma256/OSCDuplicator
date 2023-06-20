import flet as ft

from oscduplicator.duplicator import Duplicator


class OptionSettingContainer(ft.UserControl):
    """
    option settingとライセンス表示

    Attribute
    ---------
    duplicator: Duplicator
    """

    def __init__(self, duplicator: Duplicator):
        super().__init__()
        self.duplicator = duplicator

    def build(self):
        auto_transmit_setting = self.auto_transmit_checkbox()
        licence_button = self.show_licence_button()

        return ft.Container(
            content=ft.Row(
                controls=[
                    auto_transmit_setting,
                    licence_button,
                ],
                alignment=ft.MainAxisAlignment.END
            )
        )

    def auto_transmit_checkbox(self):
        return ft.Checkbox(
            label="App起動時に転送を開始",
            value=False,  # duplicator 設定を返す
            # on_change=,  # duplicator.設定を書き換える
            )
    
    def show_licence_button(self):
        return ft.TextButton(
            text="Apache License 2.0"
        )
