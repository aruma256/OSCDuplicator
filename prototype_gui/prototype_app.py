import flet as ft
from flet import UserControl, Column, Row, Text, Container


from duplicator import Duplicator
from header import Header
from receiver_field import ReceiverField
from transmitter_field import TransmitterField


class PrototypeApp(UserControl):
    """
    GUIのプロトタイプ

    Attribute
    ---------
    duplicator: Duplicator
        Appのバックエンド
    header_field: Container
        Appのヘッダー
    receiver_field: Container
        receive_portを入力する部分
    transmitter_field: Container
        transmit_portを入力する部分
    """

    def __init__(self):
        super().__init__()
        self.duplicator = Duplicator()
        self.header = Header(self.duplicator)
        self.receiver_field = ReceiverField(self.duplicator)
        self.transmitter_fields: list[
            TransmitterField
        ] = self.__init_transmitter_fields()

    def build(self):
        return Column(
            width=600,
            controls=[
                self.header,
                self.receiver_headline(),
                self.receiver_field,
                self.transmitter_headline(),
                *self.transmitter_fields,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

    def receiver_headline(self):
        return Row(controls=[Text(value="受信ポート")])

    def transmitter_headline(self):
        return Row(
            controls=[
                Container(content=Text(value="送信ポート"), margin=0, width=200),
                Container(content=Text(value="名前"), margin=0, width=300),
                Container(content=Text(value="enable"), margin=0, width=300),
            ]
        )

    def __init_transmitter_fields(self):
        if self.duplicator.settings.transmit_port_settings:
            return [
                TransmitterField(self.duplicator, i)
                for i in range(
                    len(self.duplicator.settings.transmit_port_settings)
                )
            ]
        else:
            return [TransmitterField(self.duplicator, empty=True)]
