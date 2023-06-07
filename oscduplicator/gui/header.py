import flet as ft


class Header(ft.UserControl):
    """
    GUIのヘッダー部分
    """

    def __init__(self):
        super().__init__()

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
                [self.text, self.button],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=ft.colors.INDIGO_50,
            margin=0,
        )

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
