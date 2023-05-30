import unittest.mock as mock
from queue import Empty, Queue
import pytest

from oscduplicator.osc_receiver import OSCReceiver


def test_osc_receiver_init():
    with mock.patch(
        "oscduplicator.osc_receiver.BlockingOSCUDPServer", autospec=True
    ) as mock_server:
        queue = Queue()
        receiver = OSCReceiver(5000, queue)

        assert receiver.receive_port == 5000
        assert receiver.server is mock_server.return_value
        assert receiver._message_queue is queue


def test_start_receiver():
    with mock.patch(
        "oscduplicator.osc_receiver.BlockingOSCUDPServer", autospec=True
    ) as mock_server, mock.patch(
        "oscduplicator.osc_receiver.Thread", autospec=True
    ) as mock_thread:
        receiver = OSCReceiver(5000, Queue())
        receiver.start_receiver()

        mock_thread.assert_called_once_with(
            target=mock_server.return_value.serve_forever
        )
        mock_thread.return_value.start.assert_called_once()


def test_stop_receiver():
    with mock.patch(
        "oscduplicator.osc_receiver.BlockingOSCUDPServer", autospec=True
    ) as mock_server:
        receiver = OSCReceiver(5000, Queue())
        receiver.stop_receiver()

        mock_server.return_value.shutdown.assert_called_once()


def test_q_put():
    with mock.patch(
        "oscduplicator.osc_receiver.BlockingOSCUDPServer", autospec=True
    ):
        receiver = OSCReceiver(5000, Queue())
        address = "/test"
        args = ["message"]
        receiver.q_put(address, args)

        try:
            message = receiver._message_queue.get_nowait()
        except Empty:
            pytest.fail("Queue should not be empty")

        assert message.address == address
        assert message.message == args
