import socket
from threading import Thread
from time import perf_counter, sleep

from pythonosc import dispatcher, osc_server, udp_client

from oscduplicator.duplicator import OSCDuplicator


class OscRelayIntegrationTest:
    def __init__(self) -> None:
        self.result_9003 = []
        self.result_9004 = []
        self.result_9005 = []
        self.result_9006 = []

    def run_duplicator(self):
        duplicator = OSCDuplicator()

        SAVE_FILE = "./tests/integration_tests/integration_test_Settings.json"

        duplicator.load_settings(SAVE_FILE)

        th = Thread(
            target=duplicator.transmit_msg,
            args=(duplicator.clients,),
            daemon=True,
        )
        th.start()

        duplicator.start_server()

    def launch_osc_sender(self):
        """
        OSCのクライアントを作成
        10回、pref_counterの値を送る
        """

        def __client(port: int) -> udp_client.SimpleUDPClient:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            str_ip = str(ip)
            return udp_client.SimpleUDPClient(str_ip, port)

        client = __client(9000)

        count = 0
        while count < 10:
            msg = perf_counter()
            client.send_message("/perf_counter", msg)
            sleep(0.2)
            count += 1

    def launch_osc_receivers(self):
        """
        OSCの受信サーバーを立ち上げ
        """

        def __launch_osc_receiver(port: int):
            dpt = dispatcher.Dispatcher()
            dpt.map("/*", self.osc_handler, port)

            server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", port), dpt)
            server.serve_forever()

        ports = [9003, 9004, 9005, 9006]
        receivers_thread = [
            Thread(target=__launch_osc_receiver, args=(port,))
            for port in ports
        ]

        for th in receivers_thread:
            th.start()

    def osc_handler(self, address: str, port: list[int], *args: list):
        if port[0] == 9003:
            self.result_9003.append(args[0])
        elif port[0] == 9004:
            self.result_9004.append(args[0])
        elif port[0] == 9005:
            self.result_9005.append(args[0])
        elif port[0] == 9006:
            self.result_9006.append(args[0])


def check_receiverd_value(result_: list) -> bool:
    """
    OSCの受信結果をチェックする
    チェック事項
    1. 受信した信号の個数(10個)
    2. 送信順と受信順に変化がないか

    Parameter
    ---------
    result_: list
        受信したOSC信号のリスト
    """
    if len(result_) != 10:
        return False

    for i in range(len(result_) - 1):
        if result_[i] >= result_[i + 1]:
            return False

    return True


def test_osc_relay_integration():
    test = OscRelayIntegrationTest()

    th0 = Thread(target=test.run_duplicator, daemon=True)
    th1 = Thread(target=test.launch_osc_receivers, daemon=True)
    th2 = Thread(target=test.launch_osc_sender, daemon=True)

    th0.start()
    th1.start()

    sleep(3)

    th2.start()

    sleep(3)

    assert check_receiverd_value(test.result_9003) is True
    assert check_receiverd_value(test.result_9004) is True
    assert check_receiverd_value(test.result_9005) is True
    assert len(test.result_9006) == 0
