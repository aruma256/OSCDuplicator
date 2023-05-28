import json
import pytest
from pathlib import Path
from unittest.mock import mock_open
from oscduplicator.transmit_port_setting import TransmitPortSetting
from oscduplicator.settings import Settings


@pytest.fixture
def mock_save_data():
    return {
        "receive": {
            "port": 9001
        },
        "transmit": [
            {
                "name": "test0_t",
                "port": 9001,
                "enabled": True
            },
            {
                "name": "test1_t",
                "port": 9002,
                "enabled": True
            }
        ]
    }

def test_load_json(mocker, mock_save_data):
    mock_file = mock_open(read_data=json.dumps(mock_save_data))
    mocker.patch('pathlib.Path.open', return_value=mock_file(), create=True)

    settings = Settings(Path("mock_path.json"))

    assert settings.receive_port == mock_save_data["receive"]["port"]
    assert settings.transmit_port_settings == [TransmitPortSetting(**i) for i in mock_save_data["transmit"]]


def test_get_transmit_ports(mocker, mock_save_data):
    transmit_port_settings = [TransmitPortSetting(**i) for i in mock_save_data["transmit"]]

    mocker.patch.object(Settings, 'load_json', return_value=(mock_save_data["receive"]["port"], transmit_port_settings))
    settings = Settings(Path("mock_path.json"))

    expected_port_numbers = [i["port"] for i in mock_save_data["transmit"]]
    assert settings.get_transmit_ports() == expected_port_numbers

