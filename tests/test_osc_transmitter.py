from queue import Queue
import time
from unittest.mock import Mock

from oscduplicator.osc_receiver import OSCMessage
from oscduplicator.osc_transmitter import OSCTransmitter
from oscduplicator.transmit_port_setting import TransmitPortSetting


def test_init():
    queue = Queue()
    transmitter = OSCTransmitter(queue)
    transmitter.start()
    transmitter._clients[9000] = mock_client = Mock()

    queue.put(OSCMessage("/test", (1,)))
    time.sleep(0.1)
    mock_client.send_message.assert_called_once_with("/test", (1,))
    mock_client.reset_mock()

    transmitter.pause()

    queue.put(OSCMessage("/test", (2,)))
    time.sleep(0.1)
    mock_client.send_message.assert_not_called()
    mock_client.reset_mock()


def test_start():
    transmitter = OSCTransmitter(Queue())
    transmitter.start()
    assert transmitter._running is True


def test_pause():
    transmitter = OSCTransmitter(Queue())
    transmitter.start()
    transmitter.pause()
    assert transmitter._running is False


def test_update_transmit_port():
    transmitter = OSCTransmitter(Queue())
    transmitter._clients[1234] = Mock()
    assert len(transmitter._clients) == 1

    transmitter.update_transmit_port(
        [
            TransmitPortSetting("test0", 9000, True),
            TransmitPortSetting("test1", 9001, True),
        ]
    )

    # The old client should be removed.
    # The new clients should be added.
    assert len(transmitter._clients) == 2
    assert 9000 in transmitter._clients
    assert 9001 in transmitter._clients
