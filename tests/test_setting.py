import json
from unittest.mock import Mock, mock_open

import pytest

from oscduplicator.transmit_port_setting import TransmitPortSetting
from oscduplicator.settings import Settings


@pytest.fixture
def save_data():
    return {
        "receive": {
            "port": 9001,
        },
        "transmit": [
            {
                "name": "test0_t",
                "port": 9001,
                "enabled": True,
            },
            {
                "name": "test1_t",
                "port": 9002,
                "enabled": True,
            },
        ],
    }


def test_load_json(save_data):
    mock_path = Mock()
    mock_path.open = mock_open(read_data=json.dumps(save_data))

    settings = Settings(mock_path)

    assert settings.receive_port == save_data["receive"]["port"]
    assert settings.transmit_port_settings == [
        TransmitPortSetting(**i) for i in save_data["transmit"]
    ]  # noqa


def test_get_transmit_ports(save_data):
    mock_path = Mock()
    mock_path.open = mock_open(read_data=json.dumps(save_data))

    settings = Settings(mock_path)

    settings.transmit_port_settings = [
        TransmitPortSetting(**i) for i in save_data["transmit"]
    ]  # noqa

    expected_port_numbers = [i["port"] for i in save_data["transmit"]]
    assert settings.get_transmit_ports() == expected_port_numbers
