from io import StringIO
import json
from unittest.mock import MagicMock, Mock, mock_open

from oscduplicator.settings import Settings
from oscduplicator.transmit_port_setting import TransmitPortSetting


def test_load_json():
    Settings.FILE_PATH = mock_path = Mock()
    mock_path.open = mock_open(
        read_data=json.dumps(
            {
                "receive": {
                    "port": 9001,
                },
                "transmit": [
                    {
                        "name": "app_a",
                        "port": 9002,
                        "enabled": True,
                    },
                    {
                        "name": "app_b",
                        "port": 9003,
                        "enabled": False,
                    },
                ],
            }
        )
    )

    settings = Settings()
    settings.load_json()

    assert settings.receive_port == 9001

    assert len(settings.transmit_port_settings) == 2
    assert settings.transmit_port_settings[0].name == "app_a"
    assert settings.transmit_port_settings[0].port == 9002
    assert settings.transmit_port_settings[0].enabled is True
    assert settings.transmit_port_settings[1].name == "app_b"
    assert settings.transmit_port_settings[1].port == 9003
    assert settings.transmit_port_settings[1].enabled is False


def test_save_json():
    Settings.FILE_PATH = mock_path = MagicMock()
    string_buffer = StringIO()
    mock_path.open.return_value.__enter__.return_value = string_buffer

    settings = Settings()
    settings.receive_port = 9001
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 9002, True),
        TransmitPortSetting("app_b", 9003, False),
    ]

    settings.save_json()

    assert string_buffer.getvalue() == json.dumps(
        {
            "receive": {
                "port": 9001,
            },
            "transmit": [
                {
                    "name": "app_a",
                    "port": 9002,
                    "enabled": True,
                },
                {
                    "name": "app_b",
                    "port": 9003,
                    "enabled": False,
                },
            ],
        },
        indent=4,
        ensure_ascii=False,
    )


def test_update_receive_port_setting():
    settings = Settings()
    settings.receive_port = 9000
    settings.update_receive_port_setting(9001)
    assert settings.receive_port == 9001


def test_remove_transmit_port_setting():
    settings = Settings()
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 9002, True),
        TransmitPortSetting("app_b", 9003, False),
    ]

    settings.remove_transmit_port_setting(9002)

    assert len(settings.transmit_port_settings) == 1
    assert settings.transmit_port_settings[0].name == "app_b"


def test_enable_transmit_port():
    settings = Settings()
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 9002, True),
        TransmitPortSetting("app_b", 9003, False),
    ]

    settings.enable_transmit_port(9003)
    assert settings.transmit_port_settings[1].enabled is True

    # 有効なポートを指定した場合は何もしない
    settings.enable_transmit_port(9002)
    assert settings.transmit_port_settings[0].enabled is True


def test_disable_transmit_port():
    settings = Settings()
    settings.transmit_port_settings = [
        TransmitPortSetting("app_a", 9002, True),
        TransmitPortSetting("app_b", 9003, False),
    ]

    settings.disable_transmit_port(9002)
    assert settings.transmit_port_settings[0].enabled is False

    # 無効なポートを指定した場合は何もしない
    settings.disable_transmit_port(9003)
    assert settings.transmit_port_settings[1].enabled is False
