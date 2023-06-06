import flet as ft


class ReceiverContainer(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        self.receive_port = ft.Text(value=9001)

        self.edit_button = ft.ElevatedButton(
            text="編集",
        )

        return ft.Container(
            width=600,
            padding=20,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            content=ft.Column(
                controls=[
                    ft.Text(value="受信", size=16),
                    ft.Row([self.receive_port, self.edit_button]),
                ]
            ),
        )
