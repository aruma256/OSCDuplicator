import flet as ft


class ReceiverContainer(ft.UserControl):
    """
    GUIのうちReceiverの設定部分

    Attribute
    ---------
    receive_port: int
    page_dialog: Control
        page.dialog
    """

    def __init__(self, receive_port, on_edit_button_clicked):
        super().__init__()
        self.receive_port = receive_port
        self.on_edit_button_clicked = on_edit_button_clicked

    def build(self):
        self.edit_button = ft.ElevatedButton(
            text="編集", on_click=self.on_edit_button_clicked
        )

        return ft.Container(
            width=600,
            padding=20,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            content=ft.Column(
                controls=[
                    ft.Text(value="受信", size=16),
                    ft.Row(
                        [ft.Text(value=self.receive_port), self.edit_button]
                    ),
                ]
            ),
        )
