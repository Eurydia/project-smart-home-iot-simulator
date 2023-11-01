from sensor import Sensor
from physical_quantity import PhysicalQuantity


def test_sensor_properties():
    """Test that sensorss have the correct properties."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.name == "Sensor"
    assert sensor._uuid == 0


def test_sensor_getters():
    """Test that sensors have the correct getters."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.sensor_reading() == 0
    assert sensor.sensor_kind() == PhysicalQuantity.NONE


def test_sensor_reading_is_equal_method():
    """Testing EQ mode of reading_is method."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.compare_sensor_reading("EQ", -1) is False
    assert sensor.compare_sensor_reading("EQ", 0) is True
    assert sensor.compare_sensor_reading("EQ", 1) is False


def test_sensor_reading_is_not_equal_method():
    """Testing NE mode of reading_is method."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.compare_sensor_reading("NE", -1) is True
    assert sensor.compare_sensor_reading("NE", 0) is False
    assert sensor.compare_sensor_reading("NE", 1) is True


def test_sensor_reading_is_greater_than_method():
    """Testing GT mode of reading_is method."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.compare_sensor_reading("GT", -1) is True
    assert sensor.compare_sensor_reading("GT", 0) is False
    assert sensor.compare_sensor_reading("GT", 1) is False


def test_sensor_reading_is_greater_than_or_equal_method():
    """Testing GE mode of reading_is method."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.compare_sensor_reading("GE", -1) is True
    assert sensor.compare_sensor_reading("GE", 0) is True
    assert sensor.compare_sensor_reading("GE", 1) is False


def test_sensor_reading_is_less_than_method():
    """Testing LT mode of reading_is method"""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.compare_sensor_reading("LT", -1) is False
    assert sensor.compare_sensor_reading("LT", 0) is False
    assert sensor.compare_sensor_reading("LT", 1) is True


def test_sensor_reading_is_less_than_or_equal_method():
    """Testing LE mode of reading_is method."""

    sensor: Sensor = Sensor(
        name="Sensor",
        uuid=0,
    )

    assert sensor.compare_sensor_reading("LE", -1) is False
    assert sensor.compare_sensor_reading("LE", 0) is True
    assert sensor.compare_sensor_reading("LE", 1) is True
