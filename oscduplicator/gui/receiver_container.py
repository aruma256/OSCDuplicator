import flet as ft

from oscduplicator.duplicator import Duplicator


class ReceiverContainer(ft.UserControl):
    """
    GUIのうちReceiverの設定部分

    Attribute
    ---------
    duplicator: Duplicator
    """

    def __init__(self, duplicator: Duplicator):
        super().__init__()
        self.duplicator = duplicator

    def build(self):
        self.port_text = ft.Text(value=self.duplicator.settings.receive_port)

        self.edit_button = ft.ElevatedButton(
            text="編集", on_click=self.show_receiver_edit_dialog
        )

        return ft.Container(
            width=600,
            padding=20,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            content=ft.Column(
                controls=[
                    ft.Text(value="受信", size=16),
                    ft.Row(
                        [self.port_text, self.edit_button]
                    ),
                ]
            ),
        )

    def show_receiver_edit_dialog(self, e):
        self.port_edit_field = ft.TextField(label="port", width=100)

        e.page.dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.Text("受信設定"),
                    ft.Row(
                        controls=[
                            self.port_edit_field,
                        ]
                    ),
                ],
                height=100,
            ),
            actions=[
                ft.TextButton("確定", on_click=self.on_confirm),
                ft.TextButton("キャンセル", on_click=self.on_cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        e.page.dialog.open = True
        e.page.update()

    def on_confirm(self, e):
        self.duplicator.settings.receive_port = self.port_edit_field.value
        self.port_text.value = self.duplicator.settings.receive_port
        e.page.dialog.open = False
        e.page.update()
        self.update()

    def on_cancel(self, e):
        e.page.dialog.open = False
        e.page.update()
