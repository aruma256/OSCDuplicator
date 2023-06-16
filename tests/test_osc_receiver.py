from queue import Queue
from socket import socket
from time import sleep
from unittest.mock import Mock

from pythonosc.udp_client import SimpleUDPClient

from oscduplicator.osc_receiver import OSCReceiver


def test_init():
    queue = Queue()
    receiver = OSCReceiver(5000, queue)

    assert receiver.receive_port == 5000
    assert receiver._server is None
    assert receiver._message_queue is queue


def test_start():
    with socket() as sock:
        sock.bind(("", 0))
        free_port = sock.getsockname()[1]

    receiver = OSCReceiver(free_port, Mock())
    receiver.message_handler = handler_mock = Mock()

    try:
        receiver.start()

        udp_client = SimpleUDPClient("127.0.0.1", free_port)

        udp_client.send_message("/test/0", "message")
        sleep(0.1)
        assert handler_mock.call_args[0] == ("/test/0", "message")

        udp_client.send_message("/test/1", [1, 2, 3])
        sleep(0.1)
        assert handler_mock.call_args[0] == ("/test/1", 1, 2, 3)

        udp_client.send_message("/test/2", None)
        sleep(0.1)
        assert handler_mock.call_args[0] == ("/test/2",)
    finally:
        receiver.pause()


def test_pause():
    receiver = OSCReceiver(5000, Queue())

    receiver._server = None
    receiver.pause()  # start前に呼ばれてもエラーにならない

    receiver._server = mock_server = Mock()
    receiver.pause()
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
