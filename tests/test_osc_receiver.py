from queue import Queue
from socket import socket
from time import sleep
from unittest.mock import Mock

from pythonosc.udp_client import SimpleUDPClient

from oscduplicator.osc_receiver import OSCReceiver


def test_start():
    with socket() as sock:
        sock.bind(("", 0))
        free_port = sock.getsockname()[1]

    receiver = OSCReceiver(Mock())
    receiver._receive_port = free_port
    receiver.message_handler = handler_mock = Mock()

    try:
        receiver.start()

        udp_client = SimpleUDPClient("127.0.0.1", free_port)

        udp_client.send_message("/test/0", "message")
        sleep(0.1)
        assert handler_mock.call_args[0] == ("/test/0", "message")

        udp_client.send_message("/test/1", (1, 2, 3))
        sleep(0.1)
        assert handler_mock.call_args[0] == ("/test/1", 1, 2, 3)

        udp_client.send_message("/test/2", None)
        sleep(0.1)
        assert handler_mock.call_args[0] == ("/test/2",)
    finally:
        receiver.pause()


def test_pause():
    receiver = OSCReceiver(Queue())

    receiver._server = None
    receiver.pause()  # start前に呼ばれてもエラーにならない

    receiver._server = mock_server = Mock()
    receiver.pause()
    mock_server.shutdown.assert_called_once()


def test_update_receive_port():
    receiver = OSCReceiver(Queue())
    receiver.pause = pause_mock = Mock()
    receiver.start = start_mock = Mock()

    # start前に呼ばれてもエラーにならない
    receiver._server = None
    receiver.update_receive_port(9002)
    pause_mock.assert_not_called()
    start_mock.assert_not_called()  # startしない

    receiver._server = Mock()
    receiver.update_receive_port(9003)
    pause_mock.assert_called_once()
    start_mock.assert_called_once()  # 自動的にstartする


def test_message_handler():
    queue = Queue()
    receiver = OSCReceiver(queue)

    receiver.message_handler("/test/0", "message")
    osc_message = queue.get_nowait()
    assert osc_message.address == "/test/0"
    assert osc_message.message == ("message",)

    receiver.message_handler("/test/1", 1, 2, 3)
    osc_message = queue.get_nowait()
    assert osc_message.address == "/test/1"
    assert osc_message.message == (1, 2, 3)

    receiver.message_handler("/test/2")
    osc_message = queue.get_nowait()
    assert osc_message.address == "/test/2"
    assert osc_message.message == tuple()
