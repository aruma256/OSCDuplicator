import pytest
from unittest.mock import patch
from queue import Queue
from pythonosc.udp_client import SimpleUDPClient
from oscduplicator.osc_transmitter import OSCTransmitter


class TestOSCTransmitter:
    @pytest.fixture
    def transmitter(self):
        q = Queue()
        transmitter = OSCTransmitter(q)
        return transmitter

    def test_init(self, transmitter):
        assert transmitter._OSCTransmitter__q.empty()
        assert not transmitter.is_shutdown
        assert transmitter.clients == []

    def test_init_clients(self, transmitter):
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

    def test_start_transmitter(self, transmitter):
        with patch("oscduplicator.osc_transmitter.Thread.start") as mock_start:
            transmitter.start_transmitter()
            mock_start.assert_called_once()

    def test_stop_transmitter(self, transmitter):
        transmitter.stop_transmitter()
        assert transmitter.is_shutdown
