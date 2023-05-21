import pytest

from oscduplicator.setting import TransmitPortSetting


class TestTransmitPortSetting:
    def test_init_valid(self):
        tps = TransmitPortSetting("Test", 8080, True)
        assert tps.name == "Test"
        assert tps.port == 8080
        assert tps.enabled is True

    def test_init_transforms_name(self):
        tps = TransmitPortSetting(1234, 8080, True)
        assert tps.name == "1234"

    def test_invalid_port_raises_exception(self):
        with pytest.raises(ValueError):
            TransmitPortSetting("Test", 70000, True)

    def test_invalid_enabled_raises_exception(self):
        with pytest.raises(TypeError):
            TransmitPortSetting("Test", 8080, "True")

    def test_set_invalid_port_raises_exception(self):
        tps = TransmitPortSetting("Test", 8080, True)
        with pytest.raises(ValueError):
            tps.port = 70000

    def test_set_invalid_enabled_raises_exception(self):
        tps = TransmitPortSetting("Test", 8080, True)
        with pytest.raises(TypeError):
            tps.enabled = "True"

    def test_set_transforms_name(self):
        tps = TransmitPortSetting("Test", 8080, True)
        tps.name = 1234
        assert tps.name == "1234"
