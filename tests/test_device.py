from src.device import BASIC_SMART_LIGHT
from src.physical_quantity import PhysicalQuantity


def test_device_properties():
    """Test that the device properties are set correctly."""
    assert BASIC_SMART_LIGHT.uuid == 100001
    assert BASIC_SMART_LIGHT.device_value_range == (0, 100)
    assert BASIC_SMART_LIGHT.device_kind == PhysicalQuantity.BRIGHTNESS
    assert BASIC_SMART_LIGHT.device_value == 0


def test_device_getters():
    """Test that the device getters are set correctly."""

    assert (
        BASIC_SMART_LIGHT.get_loggable_text(False)
        == "Basic smart light: current BRIGHTNESS (%) is 0."
    )
    assert (
        BASIC_SMART_LIGHT.set_device_value(50)
        == "Basic smart light: current BRIGHTNESS (%) is 50."
    )
