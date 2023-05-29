import random
import string
from threading import Thread
from time import sleep

from pythonosc import osc_server

from oscduplicator.duplicator import OSCDuplicator
from oscduplicator.transmit_port_setting import TransmitPortSetting


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
            __server_is_shut_down(self.osc_duplicator._OSCDuplicator__server)
            is False
        )
        self.osc_duplicator.stop_server()
        sleep(1)
        assert (
            __server_is_shut_down(self.osc_duplicator._OSCDuplicator__server)
            is True
        )

    def __transmit_port_settings(self):
        """
        transmit_port_settingsのゲッター
        """
        return self.osc_duplicator._OSCDuplicator__transmit_port_settings

    def test_load_settings(self):
        """
        正しくjsonファイルを読み込めるかテスト
        """
        # Arrange
        FILE_PATH = "./tests/test_Settings.json"
        # Act
        self.osc_duplicator.load_settings(FILE_PATH)
        # Assert
        assert self.osc_duplicator.receive_port == 9001

        assert self.__transmit_port_settings()[0].name == "test0_t"
        assert self.__transmit_port_settings()[0].port == 9001
        assert self.__transmit_port_settings()[0].enabled is True

        assert self.__transmit_port_settings()[1].name == "test1_t"
        assert self.__transmit_port_settings()[1].port == 9002
        assert self.__transmit_port_settings()[1].enabled is True

        assert self.__transmit_port_settings()[4].name == "test4_f"
        assert self.__transmit_port_settings()[4].port == 9004
        assert self.__transmit_port_settings()[4].enabled is False

        print(len(self.osc_duplicator.clients))

        assert set(
            client._port for client in self.osc_duplicator.clients
        ) == set([9001, 9002, 9003])

    def test_update_settings(self):
        """
        class Duplicatorの設定を書き換えれるかテスト
        """

        def __random_name():
            return "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

        def __random_port():
            return random.randrange(start=0, stop=65535, step=1)

        # Arrange
        new_receive_port = 8001
        new_transmit_port_settings = [
            TransmitPortSetting(__random_name(), __random_port(), True)
            for _ in range(4)
        ]

        # Act
        self.osc_duplicator.update_settings(
            new_receive_port, new_transmit_port_settings
        )

        # Assert
        assert self.osc_duplicator.receive_port == 8001

        assert (
            self.__transmit_port_settings()[0].name
            == new_transmit_port_settings[0].name
        )
        assert (
            self.__transmit_port_settings()[0].port
            == new_transmit_port_settings[0].port
        )
        assert self.__transmit_port_settings()[0].enabled is True
        assert (
            self.__transmit_port_settings()[3].name
            == new_transmit_port_settings[3].name
        )
        assert (
            self.__transmit_port_settings()[3].port
            == new_transmit_port_settings[3].port
        )
        assert self.__transmit_port_settings()[3].enabled is True

        assert set(
            client._port for client in self.osc_duplicator.clients
        ) == set([tps.port for tps in new_transmit_port_settings])

    def test_save_settings(self):
        """
        正しくjsonファイルを書き出せるかテスト
        """

        def __random_name():
            return "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

        def __random_port():
            return random.randrange(start=0, stop=65535, step=1)

        # Arrange
        new_receive_port = 8001
        new_transmit_port_settings = [
            TransmitPortSetting(__random_name(), __random_port(), True)
            for _ in range(4)
        ]

        # Act
        SAVE_FILE_PATH = "./tests/test_save_Settings.json"
        self.osc_duplicator.update_settings(
            new_receive_port, new_transmit_port_settings
        )
        self.osc_duplicator.save_settings(SAVE_FILE_PATH)

        self.osc_duplicator.load_settings(SAVE_FILE_PATH)

        # Assert
        assert self.osc_duplicator.receive_port == 8001

        assert (
            self.__transmit_port_settings()[0].name
            == new_transmit_port_settings[0].name
        )
        assert (
            self.__transmit_port_settings()[0].port
            == new_transmit_port_settings[0].port
        )
        assert self.__transmit_port_settings()[0].enabled is True
        assert (
            self.__transmit_port_settings()[3].name
            == new_transmit_port_settings[3].name
        )
        assert (
            self.__transmit_port_settings()[3].port
            == new_transmit_port_settings[3].port
        )
        assert self.__transmit_port_settings()[3].enabled is True

    # def test_transmit_msg(self):
    #     """
    #     キューからOSC信号を取り出し、転送できるかテストする
    #     """
    #     pass
