from queue import Queue
from unittest.mock import patch

from pythonosc.udp_client import SimpleUDPClient

from oscduplicator.osc_transmitter import OSCTransmitter


def test_init():
    queue = Queue()
    transmitter = OSCTransmitter(queue)
    assert transmitter._q is queue
    assert not transmitter.is_shutdown
    assert len(transmitter.clients) == 0


def test_init_clients():
    transmitter = OSCTransmitter(Queue())
    with patch(
        "oscduplicator.osc_transmitter.socket.gethostname",
        return_value="localhost",
    ), patch(
        "oscduplicator.osc_transmitter.socket.gethostbyname",
        return_value="127.0.0.1",
    ):
        transmitter.transmit_ports = [8000, 8001]
        clients = transmitter.init_clients(transmitter.transmit_ports)
        assert len(clients) == 2
        for client in clients:
            assert isinstance(client, SimpleUDPClient)


def test_start_transmitter():
    transmitter = OSCTransmitter(Queue())
    with patch("oscduplicator.osc_transmitter.Thread.start") as mock_start:
        transmitter.start_transmitter()
        mock_start.assert_called_once()


def test_stop_transmitter():
    transmitter = OSCTransmitter(Queue())
    transmitter.stop_transmitter()
    assert transmitter.is_shutdown
