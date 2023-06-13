import flet as ft


APP_TITLE = "OSCDuplicator"


class App:
    def main(self, page: ft.Page):
        page.title = APP_TITLE
        page.horizontal_alignment = "center"
        page.window_width, page.window_height = 600, 800
        page.add(self.create_header())

    def create_header(self) -> ft.Control:
        return ft.Container(
            width=600,
            height=80,
            content=ft.Row(
                [
                    ft.Text(
                        value="Duplicator stopped",
                        size=40,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ElevatedButton(
                        text="stop",
                        bgcolor=ft.colors.LIGHT_GREEN_ACCENT_400,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=ft.colors.INDIGO_50,
            margin=0,
        )


def start():
    ft.app(target=App().main)
