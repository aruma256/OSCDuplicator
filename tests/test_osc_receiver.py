from unittest.mock import Mock, patch
from queue import Queue

from oscduplicator.osc_receiver import OSCReceiver


def test_init():
    queue = Queue()
    receiver = OSCReceiver(5000, queue)

    assert receiver.receive_port == 5000
    assert receiver._server is None
    assert receiver._message_queue is queue


def test_start():
    with patch(
        "oscduplicator.osc_receiver.BlockingOSCUDPServer", autospec=True
    ) as mock_server, patch(
        "oscduplicator.osc_receiver.Thread", autospec=True
    ) as mock_thread:
        receiver = OSCReceiver(5000, Queue())
        receiver.start()

        mock_thread.assert_called_once_with(
            target=mock_server.return_value.serve_forever
        )
        mock_thread.return_value.start.assert_called_once()


def test_stop():
    receiver = OSCReceiver(5000, Queue())

    receiver._server = None
    receiver.stop()  # start前に呼ばれてもエラーにならない

    receiver._server = mock_server = Mock()
    receiver.stop()
    mock_server.shutdown.assert_called_once()


def test_message_handler():
    queue = Queue()
    receiver = OSCReceiver(5000, queue)
    address = "/test"
    args = ["message"]
    receiver.message_handler(address, args)

    assert queue.qsize() == 1

    message = receiver._message_queue.get_nowait()

    assert message.address == address
    assert message.message == args
