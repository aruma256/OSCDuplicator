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

    receiver_mock.stop.assert_called_once()
    transmitter_mock.pause.assert_called_once()


@pytest.mark.skip(reason="テスト未実装")  # TODO テストしやすい実装に書き換えてからテストを追加する
def test_save_settings():
    pass
