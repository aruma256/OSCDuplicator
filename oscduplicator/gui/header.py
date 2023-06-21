import flet as ft

from oscduplicator.duplicator import Duplicator


class Header(ft.UserControl):
    """
    GUIのヘッダー部分
    """

    def __init__(self, duplicator: Duplicator):
        super().__init__()
        self.duplicator = duplicator

    def build(self):
        self.text = ft.Text(
            value="Duplicator stopped", size=40, weight=ft.FontWeight.BOLD
        )

        self.button = ft.ElevatedButton(
            text="stop",
            bgcolor=ft.colors.LIGHT_GREEN_ACCENT_400,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            color=ft.colors.WHITE,
        )

        return ft.Container(
            width=600,
            height=80,
            content=ft.Row(
                [self.text, self.button, self.popup_menu()],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=ft.colors.INDIGO_50,
            margin=0,
        )

    def popup_menu(self):
        return ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(content=self.auto_transmit_checkbox()),
                ft.PopupMenuItem(
                    text="ライセンス", on_click=self.show_license_list_dialog
                ),
            ]
        )

    def show_option_setting_dialog(self, e):
        e.page.dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[ft.Text("オプション設定"), self.auto_transmit_checkbox()],
                height=100,  # ここ自動調整できない...?
            )
        )
        e.page.dialog.open = True
        e.page.update()

    def auto_transmit_checkbox(self):
        return ft.Checkbox(
            label="App起動時に転送を開始",
            # value=,
            # on_chenge=,
        )

    def show_license_list_dialog(self, e):
        e.page.dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[ft.Text("ライセンス"), *self._license_list()],
                height=100,  # ここ自動調整できない...?
            ),
        )
        e.page.dialog.open = True
        e.page.update()

    def _license_list(self):
        lib_list = [
            [
                "このアプリ:",
                "Apache License 2.0",
                "https://github.com/aruma256/OSCDuplicator/blob/main/LICENSE",
            ],
        ]

        return [
            ft.Row([ft.Text(lib[0]), ft.TextButton(text=lib[1])])
            for lib in lib_list
        ]

    def update_status_text(self):
        """
        dupkicatorの実行状態に応じて、
        テキストを変更
        """
        if not False:
            self.text.value = "Duplicator stopped"
        else:
            self.text.value = "Duplicator started"

    def update_run_button(self):
        """
        dupkicatorの実行状態に応じて、
        ボタンのテキスト・レイアウトを変更
        """
        if not False:
            self.button.text = "start"
            self.button.bgcolor = ft.colors.LIGHT_GREEN_ACCENT_400

        else:
            self.button.text = "stop"
            self.button.bgcolor = ft.colors.RED
