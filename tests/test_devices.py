from src.devices.device import Device
from src.sensors.quantity import QuantityKind


def test_device_properties():
    """Test that the device properties are set correctly."""

    device: Device = Device(
        name="test",
        uuid=1,
    )

    assert device.name == "test"
    assert device.uuid == 1


def test_device_getters():
    """Test that the device getters are set correctly."""

    device: Device = Device(
        name="test",
        uuid=1,
    )

    assert device.get_device_value() == 0
    assert device.get_device_kind() == QuantityKind.NONE
    assert device.get_device_value_range() == (0, 100)
