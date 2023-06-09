import flet as ft


class TransmitterContainer(ft.UserControl):
    """
    GUIのうちTransmitterの設定部分

    attribute
    ---------
    transmittter_settings: list
        転送設定, [[port, name, enabled]]

    """

    def __init__(self):
        super().__init__()
        self.transmitter_settings: list = []

    def build(self):
        return ft.Container(
            width=600,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(value="転送, size=16"),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("port")),
                            ft.DataColumn(ft.Text("名前")),
                            ft.DataColumn(ft.Text("有効化")),
                            ft.DataColumn(ft.Text("")),
                        ],
                        rows=self.data_table_rows(),
                    ),
                    ft.ElevatedButton(
                        text="追加",
                        icon=ft.icons.ADD,
                        width=440,
                        on_click=self.show_transmitter_add_dlg,
                    ),
                ]
            ),
        )

    def data_table_rows(self) -> list:
        """
        self.transmitter_settingsから,
        DataTableに表示するためのDataRowのリストを作成する
        """

        def create_row(port="", name="", enabled=False):
            return ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(value=port)),
                    ft.DataCell(ft.Text(value=name)),
                    ft.DataCell(ft.Checkbox(value=enabled)),
                    ft.DataCell(
                        ft.ElevatedButton(
                            text="編集", on_click=self.show_transmitter_edit_dlg
                        )
                    ),
                ]
            )

        if not self.transmitter_settings:
            return [create_row()]
        else:
            return [
                create_row(setting[0], setting[1], setting[2])
                for setting in self.transmitter_settings
            ]

    def show_transmitter_edit_dlg(self, e):
        e.page.dialog = ft.AlertDialog(
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
                ft.TextButton("確定", on_click=self.close_dlg),
                ft.TextButton("キャンセル", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        e.page.dialog.open = True
        e.page.update()

    def show_transmitter_add_dlg(self, e):
        e.page.dialog = ft.AlertDialog(
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
                ft.TextButton("追加", on_click=self.close_dlg),
                ft.TextButton("キャンセル", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        e.page.dialog.open = True
        e.page.update()

    def close_dlg(self, e):
        e.page.dialog.open = False
        e.page.update()
