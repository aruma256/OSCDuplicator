from threading import Thread
from time import sleep

import pytest
from pythonosc import osc_server

from oscduplicator.duplicator import OSCDuplicator, TransmitPortSetting


class TestDuplicator:
    osc_duplicator = OSCDuplicator()
    # def test_start_server(self):
    #     """
    #     サーバーを起動できるかテスト
    #     """
    #     pass

    def test_start_stop_server(self):
        """
        サーバーを起動・停止できるかテスト
        """

        def __server_is_shut_down(server: osc_server.ThreadingOSCUDPServer):
            """
            サーバーがシャットダウンしているかどうか判定する
            """
            return server._BaseServer__is_shut_down.is_set()

        assert self.osc_duplicator.receive_port is None

        self.osc_duplicator.receive_port = 9001

        assert self.osc_duplicator.receive_port == 9001

        th = Thread(target=self.osc_duplicator.start_server, daemon=True)
        th.start()

        sleep(1)
        assert (
            __server_is_shut_down(self.osc_duplicator._OSCDuplicator__server) is False
        )
        self.osc_duplicator.stop_server()
        sleep(1)
        assert __server_is_shut_down(self.osc_duplicator._OSCDuplicator__server) is True

    def test_load_settings(self):
        """
        正しくjsonファイルを読み込めるかテスト
        """
        pass

    def test_update_settings(self):
        """
        class Duplicatorの設定を書き換えれるかテスト
        """
        pass

    def test_save_settings(self):
        """
        正しくjsonファイルを書き出せるかテスト
        """
        pass

    def test_transmit_msg(self):
        """
        キューからOSC信号を取り出し、転送できるかテストする
        """
        pass
