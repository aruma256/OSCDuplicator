from io import StringIO
import json
from unittest.mock import MagicMock, Mock, mock_open

from oscduplicator.settings import Settings
from oscduplicator.transmit_port_setting import TransmitPortSetting


def test_load():
    Settings.FILE_PATH = mock_path = Mock()
    mock_path.open = mock_open(
        read_data=json.dumps(
            {
                "receive": {
                    "port": 10001,
                },
                "transmit": [
                    {
                        "name": "app_a",
                        "port": 10002,
                        "enabled": True,
                    },
                    {
                        "name": "app_b",
                        "port": 10003,
                        "enabled": False,
                    },
                ],
                "auto_start": False
            }
        )
    )

    settings = Settings()

    # ファイルが存在しない場合
    mock_path.exists.return_value = False
    settings.load()

    assert settings.receive_port == 9001

    # ファイルが存在する場合
    mock_path.exists.return_value = True
    settings.load()

    assert settings.receive_port == 10001
    assert len(settings.transmit_port_settings) == 2
    assert settings.transmit_port_settings[0].name == "app_a"
    assert settings.transmit_port_settings[0].port == 10002
    assert settings.transmit_port_settings[0].enabled is True
    assert settings.transmit_port_settings[1].name == "app_b"
    assert settings.transmit_port_settings[1].port == 10003
    assert settings.transmit_port_settings[1].enabled is False


def test_save_json():
    Settings.FILE_PATH = mock_path = MagicMock()
    string_buffer = StringIO()
    mock_path.open.return_value.__enter__.return_value = string_buffer

    settings = Settings()
    settings.update_receive_port_setting(10001)
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 10002, True),
        TransmitPortSetting("app_b", 10003, False),
    ]
    settings.auto_start = False

    settings.save_json()

    assert string_buffer.getvalue() == json.dumps(
        {
            "receive": {
                "port": 10001,
            },
            "transmit": [
                {
                    "name": "app_a",
                    "port": 10002,
                    "enabled": True,
                },
                {
                    "name": "app_b",
                    "port": 10003,
                    "enabled": False,
                },
            ],
            "auto_start": False
        },
        indent=4,
        ensure_ascii=False,
    )


def test_update_receive_port_setting():
    settings = Settings()
    settings.update_receive_port_setting(10001)

    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 10002, True),
        TransmitPortSetting("app_b", 10003, False),
    ]

    assert settings.update_receive_port_setting(10004) is True
    assert settings.receive_port == 10004

    # 同一ポート番号を指定した場合は更新しない
    assert settings.update_receive_port_setting(10004) is False
    assert settings.receive_port == 10004

    # 送信先に含まれるポート番号を指定した場合は更新しない
    assert settings.update_receive_port_setting(10003) is False
    assert settings.receive_port == 10004


def test_add_transmit_port_setting():
    settings = Settings()
    settings.update_receive_port_setting(10001)
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 10002, True),
        TransmitPortSetting("app_b", 10003, False),
    ]

    assert settings.add_transmit_port_setting("app_c", 10004, True) is True
    assert len(settings.transmit_port_settings) == 3

    # 重複するポート番号を指定した場合は追加しない
    assert settings.add_transmit_port_setting("app_d", 10002, True) is False
    assert len(settings.transmit_port_settings) == 3

    # 受信と同一ポート番号を指定した場合は追加しない
    assert settings.add_transmit_port_setting("app_e", 10001, True) is False
    assert len(settings.transmit_port_settings) == 3


def test_remove_transmit_port_setting():
    settings = Settings()
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 10002, True),
        TransmitPortSetting("app_b", 10003, False),
    ]

    settings.remove_transmit_port_setting(10002)

    assert len(settings.transmit_port_settings) == 1
    assert settings.transmit_port_settings[0].name == "app_b"


def test_enable_transmit_port():
    settings = Settings()
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 10002, True),
        TransmitPortSetting("app_b", 10003, False),
    ]

    settings.enable_transmit_port(10003)
    assert settings.transmit_port_settings[1].enabled is True

    # 有効なポートを指定した場合は何もしない
    settings.enable_transmit_port(10002)
    assert settings.transmit_port_settings[0].enabled is True


def test_disable_transmit_port():
    settings = Settings()
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 10002, True),
        TransmitPortSetting("app_b", 10003, False),
    ]

    settings.disable_transmit_port(10002)
    assert settings.transmit_port_settings[0].enabled is False

    # 無効なポートを指定した場合は何もしない
    settings.disable_transmit_port(10003)
    assert settings.transmit_port_settings[1].enabled is False
