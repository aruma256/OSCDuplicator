from threading import Thread
from time import sleep

import pytest
from pythonosc import osc_server

from oscduplicator.duplicator import OSCDuplicator, TransmitPortSetting


class TestTransmitPortSettings:
    def test_init_TransmitPortSettings(self):
        """
        TransmitPortSettingが不正な値に対して例外を出せるかテスト
        """

        # correct data
        port_settings = TransmitPortSetting("Port0", 9000, True)
        assert port_settings.name == "Port0"
        assert port_settings.port == 9000
        assert port_settings.enabled is True

        # incorrect data type
        with pytest.raises(TypeError):
            TransmitPortSetting(123, 9000, False)

        with pytest.raises(TypeError):
            TransmitPortSetting("設定", "9000", True)

        # incorrect data value
        with pytest.raises(ValueError):
            TransmitPortSetting("koya_so", -1, True)

        with pytest.raises(ValueError):
            TransmitPortSetting("koya_so", 65536, True)

        with pytest.raises(TypeError):
            TransmitPortSetting("nyanko", 8000, "neko")


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
