import flet as ft


from oscduplicator.gui.header import Header
from oscduplicator.gui.receiver_container import ReceiverContainer
from oscduplicator.gui.transmitter_container import TransmitterContainer

APP_TITLE = "OSCDuplicator"


class App:
    def main(self, page: ft.Page):
        def show_receiver_edit_dlg(_):
            page.dialog = ft.AlertDialog(
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
                    ft.TextButton("確定", on_click=close_dlg),
                    ft.TextButton("キャンセル", on_click=close_dlg),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog.open = True
            page.update()

        def show_transmitter_edit_dlg(_):
            page.dialog = ft.AlertDialog(
                content=ft.Column(
                    controls=[
                        ft.Text("転送設定"),
                        ft.Row(
                            controls=[
                                ft.TextField(label="port", width=100),
                                ft.TextField(label="name", width=100),
                            ]
                        ),
                    ],
                    height=100,
                ),
                actions=[
                    ft.TextButton("確定", on_click=close_dlg),
                    ft.TextButton("キャンセル", on_click=close_dlg),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog.open = True
            page.update()

        def close_dlg(_):
            page.dialog.open = False
            page.update()

        page.title = APP_TITLE
        page.horizontal_alignment = "center"
        page.window_width, page.window_height = 600, 800

        self.header = Header()
        self.receiver_container = ReceiverContainer(
            9001, show_receiver_edit_dlg
        )  # ポートは仮
        self.transmitter_container = TransmitterContainer(
            show_transmitter_edit_dlg
        )

        page.add(self.header)
        page.add(self.receiver_container)
        page.add(self.transmitter_container)


def start():
    ft.app(target=App().main)


if __name__ == "__main__":
    start()
