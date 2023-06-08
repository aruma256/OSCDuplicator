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

    def __init__(self, receive_port):
        super().__init__()
        self.receive_port = receive_port

    def build(self):
        self.edit_button = ft.ElevatedButton(
            text="編集", on_click=self.show_receiver_edit_dlg
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

    def show_receiver_edit_dlg(self, e):
        e.page.dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.Text("受信設定"),
                    ft.Row(
                        controls=[
                            ft.TextField(label="port", width=100),
                        ]
                    ),
                ],
                height=100,
            ),
            actions=[
                ft.TextButton("確定", on_click=self.close_dlg),
                ft.TextButton("キャンセル", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        print(type(e))
        e.page.dialog.open = True
        e.page.update()

    def close_dlg(self, e):  # 仮
        e.page.dialog.open = False
        e.page.update()
