import flet as ft
from typing import Callable

from duplicator import Duplicator


class TransmitterContainer(ft.UserControl):
    def __init__(self, duplicator: Duplicator, on_edit_clicked: Callable):
        super().__init__()
        self.duplicator = duplicator
        self.on_edit_clicked = on_edit_clicked
        self.transmitter_settings = self.init_transmitter_settings()

    def build(self):
        return ft.Container(
            width=600,
            bgcolor=ft.colors.LIGHT_BLUE_50,
            content=ft.Column(
                controls=[
                    ft.Text(value="転送", size=16),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("port")),
                            ft.DataColumn(ft.Text("名前")),
                            ft.DataColumn(ft.Text("有効化")),
                            ft.DataColumn(ft.Text("")),
                        ],
                        rows=self.DataTableRows(),
                    ),
                ]
            ),
        )

    def DataTableRows(self):
        def cell(port="", name="", enabled=False):
            return ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(value=port)),
                    ft.DataCell(ft.Text(value=name)),
                    ft.DataCell(ft.Checkbox(value=enabled)),
                    ft.DataCell(ft.ElevatedButton(text="編集")),
                ]
            )

        if not self.transmitter_settings:
            return [cell()]

        else:
            return [
                cell(setting[0], setting[1], setting[2])
                for setting in self.transmitter_settings
            ]

    def init_transmitter_settings(self):
        transmitter_settings = []

        settings = self.duplicator.settings.transmit_port_settings

        if settings:
            transmitter_settings = [
                [setting.port, setting.name, setting.enabled]
                for setting in settings
            ]

        return transmitter_settings
