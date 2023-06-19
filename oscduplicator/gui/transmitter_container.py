import flet as ft
from functools import partial

from oscduplicator.duplicator import Duplicator


class TransmitterContainer(ft.UserControl):
    """
    GUIのうちTransmitterの設定部分

    attribute
    ---------
    transmittter_settings: list
        転送設定, [[port, name, enabled]]

    """

    def __init__(self, duplicator: Duplicator):
        super().__init__()
        self.duplicator = duplicator

    def build(self):
        self.transmitter_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("port")),
                ft.DataColumn(ft.Text("名前")),
                ft.DataColumn(ft.Text("有効化")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=self.data_table_rows(),
        )

        return ft.Container(
            width=600,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(value="転送", size=16),
                    self.transmitter_data_table,
                    ft.ElevatedButton(
                        text="追加",
                        icon=ft.icons.ADD,
                        width=440,
                        on_click=self.show_transmitter_add_dialog,
                    ),
                ]
            ),
        )

    def data_table_rows(self) -> list:
        """
        self.transmitter_settingsから,
        DataTableに表示するためのDataRowのリストを作成する
        """
        return [
            self.create_row(setting[0], setting[1], setting[2])
            for setting in self.duplicator.settings.transmit_port_settings
        ]

    def create_row(self, port="", name="", enabled=False):
        port_text_field = ft.Text(value=port)
        name_text_field = ft.Text(value=name)
        checkbox = ft.Checkbox(value=enabled)
        checkbox.on_change = partial(
            self.on_check_box_change, checkbox, port_text_field
        )

        return ft.DataRow(
            cells=[
                ft.DataCell(port_text_field),
                ft.DataCell(name_text_field),
                ft.DataCell(checkbox),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER,
                        on_click=partial(
                            self.on_delete_clicked, port_text_field
                        ),
                    )
                ),
            ]
        )

    def show_transmitter_add_dialog(self, e):
        port_text_field = ft.TextField(label="port", width=100)
        name_text_field = ft.TextField(label="name", width=100)

        e.page.dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.Text("転送設定"),
                    ft.Row(
                        controls=[
                            port_text_field,
                            name_text_field,
                        ]
                    ),
                ],
                height=100,
            ),
            actions=[
                ft.TextButton(
                    "追加",
                    on_click=partial(
                        self.on_add_confirm, port_text_field, name_text_field
                    ),
                ),
                ft.TextButton("キャンセル", on_click=self.on_cancel),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        e.page.dialog.open = True
        e.page.update()

    def on_add_confirm(self, port_text_field, name_text_field, e):
        port = int(port_text_field.value)
        name = name_text_field.value

        row = self.create_row(port, name, False)
        self.transmitter_data_table.rows.append(row)

        self.duplicator.add_transmit_port(name, port)

        e.page.dialog.open = False
        e.page.update()
        self.update()

    def on_delete_clicked(self, port_text_field, _):
        port = port_text_field.value

        self.duplicator.remove_transmit_port(port)

        self.transmitter_data_table.rows = self.data_table_rows()

        self.update()

    def on_cancel(self, e):
        e.page.dialog.open = False
        e.page.update()

    def on_check_box_change(self, checkbox, port_text_field, _):
        enabled = checkbox.value
        port = int(port_text_field.value)

        if enabled:
            self.duplicator.settings.enable_transmit_port(port)
            self.duplicator.transmitter.add_destination_port(port)
        else:
            self.duplicator.settings.disable_transmit_port(port)
            self.duplicator.transmitter.remove_destination_port(port)

        # print(self.duplicator.settings.transmit_port_settings)
        # print(self.duplicator.transmitter._clients)
        self.update()
