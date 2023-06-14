from unittest.mock import Mock

from oscduplicator.duplicator import Duplicator


def test_stop_duplicate():
    duplicator = Duplicator()
    duplicator.receiver = receiver_mock = Mock()
    duplicator.transmitter = transmitter_mock = Mock()

    duplicator.stop_duplicate()

    receiver_mock.stop.assert_called_once()
    transmitter_mock.pause.assert_called_once()
