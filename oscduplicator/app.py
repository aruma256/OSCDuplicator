import flet as ft


APP_TITLE = "OSCDuplicator"


class App:
    def main(self, page: ft.Page):
        page.title = APP_TITLE

        self._app_bar = ft.AppBar(
            title=ft.Text(APP_TITLE),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self._sample_text = ft.Text("sample aaaa")
        page.controls.extend(
            [
                self._app_bar,
                self._sample_text,
            ],
        )
        page.update()


def start():
    ft.app(target=App().main)
