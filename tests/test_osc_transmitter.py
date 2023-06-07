from queue import Queue
import time
from unittest.mock import Mock

from oscduplicator.osc_receiver import OSCMessage
from oscduplicator.osc_transmitter import OSCTransmitter


def test_init():
    queue = Queue()
    transmitter = OSCTransmitter(queue)
    transmitter.start()
    transmitter._clients[9000] = mock_client = Mock()

    queue.put(OSCMessage("/test", 1))
    time.sleep(0.1)
    mock_client.send_message.assert_called_once_with("/test", 1)
    mock_client.reset_mock()

    transmitter.pause()

    queue.put(OSCMessage("/test", 2))
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


def test_add_destination_port():
    transmitter = OSCTransmitter(Queue())

    # Add a new port
    port1 = 8000
    assert transmitter.add_destination_port(port1) is True

    # Add the same port again
    assert transmitter.add_destination_port(port1) is False

    # Add a different port
    port2 = 9000
    assert transmitter.add_destination_port(port2) is True

    # Check if the clients dictionary is updated correctly
    assert port1 in transmitter._clients
    assert port2 in transmitter._clients
    assert len(transmitter._clients) == 2

    # Check if the SimpleUDPClient instances are created correctly
    assert transmitter._clients[port1]._address == OSCTransmitter.ADDRESS
    assert transmitter._clients[port1]._port == port1
    assert transmitter._clients[port2]._address == OSCTransmitter.ADDRESS
    assert transmitter._clients[port2]._port == port2


def test_remove_destination_port():
    transmitter = OSCTransmitter(Queue())

    # Add ports
    port1 = 8000
    port2 = 9000
    transmitter.add_destination_port(port1)
    transmitter.add_destination_port(port2)
    assert len(transmitter._clients) == 2

    # Remove a port that exists
    transmitter.remove_destination_port(port1)
    assert port1 not in transmitter._clients
    assert len(transmitter._clients) == 1

    # Remove a port that doesn't exist
    non_existing_port = 10000
    #   Should not raise an error
    transmitter.remove_destination_port(non_existing_port)
    assert len(transmitter._clients) == 1

    # Check if the other port still exists
    assert port2 in transmitter._clients
