from unittest.mock import Mock

import pytest

from oscduplicator.duplicator import Duplicator


@pytest.mark.skip(reason="テスト未実装")  # TODO テストしやすい実装に書き換えてからテストを追加する
def test_start_duplicate():
    pass


def test_stop_duplicate():
    duplicator = Duplicator()
    duplicator.receiver = receiver_mock = Mock()
    duplicator.transmitter = transmitter_mock = Mock()

    duplicator.stop_duplicate()

    receiver_mock.pause.assert_called_once()
    transmitter_mock.pause.assert_called_once()


@pytest.mark.skip(reason="テスト未実装")  # TODO テストしやすい実装に書き換えてからテストを追加する
def test_save_settings():
    pass


def test_add_transmit_port():
    duplicator = Duplicator()
    duplicator.settings = settings_mock = Mock()
    duplicator.transmitter = transmitter_mock = Mock()

    settings_mock.add_transmit_port_setting.return_value = False
    duplicator.add_transmit_port("test", 9002)
    transmitter_mock.update_transmit_port.assert_not_called()

    settings_mock.add_transmit_port_setting.return_value = True
    duplicator.add_transmit_port("test", 9002)
    transmitter_mock.update_transmit_port.assert_called_once_with(
        settings_mock.transmit_port_settings,
    )


def test_remove_transmit_port():
    duplicator = Duplicator()
    duplicator.settings = settings_mock = Mock()
    duplicator.transmitter = transmitter_mock = Mock()

    duplicator.remove_transmit_port(9002)

    settings_mock.remove_transmit_port_setting.assert_called_once_with(9002)
    transmitter_mock.update_transmit_port.assert_called_once_with(
        settings_mock.transmit_port_settings,
    )
