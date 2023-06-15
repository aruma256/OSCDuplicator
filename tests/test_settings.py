import json
from unittest.mock import Mock, mock_open

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


def test_get_transmit_ports():
    settings = Settings()

    settings.transmit_port_settings = [
        TransmitPortSetting(name="app_a", port=9002, enabled=True),
        TransmitPortSetting(name="app_b", port=9003, enabled=False),
    ]

    assert settings.get_transmit_ports() == [9002, 9003]
