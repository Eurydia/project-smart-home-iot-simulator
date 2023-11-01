from src.sensor import BASIC_DAYLIGHT_SENSOR
from src.physical_quantity import PhysicalQuantity


def test_sensor_properties():
    """Test that sensorss have the correct properties."""

    assert BASIC_DAYLIGHT_SENSOR.uuid == 3
    assert BASIC_DAYLIGHT_SENSOR.sensor_kind == PhysicalQuantity.BRIGHTNESS
    assert BASIC_DAYLIGHT_SENSOR.sensor_reading == 0
    assert BASIC_DAYLIGHT_SENSOR.sensor_reading_range == (0, 100)


def test_sensor_getters():
    """Test that sensors have the correct getters."""

    assert (
        BASIC_DAYLIGHT_SENSOR.get_loggable_text(False)
        == "Basic daylight sensor: current BRIGHTNESS (%) reading is 0."
    )

    # assert BASIC_DAYLIGHT_SENSOR.update_sensor_value()


def test_sensor_reading_is_equal_method():
    """Testing EQ mode of reading_is method."""

    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("EQ", -1) is False
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("EQ", 0) is True
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("EQ", 1) is False


def test_sensor_reading_is_not_equal_method():
    """Testing NE mode of reading_is method."""

    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("NE", -1) is True
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("NE", 0) is False
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("NE", 1) is True


def test_sensor_reading_is_greater_than_method():
    """Testing GT mode of reading_is method."""

    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("GT", -1) is True
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("GT", 0) is False
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("GT", 1) is False


def test_sensor_reading_is_greater_than_or_equal_method():
    """Testing GE mode of reading_is method."""

    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("GE", -1) is True
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("GE", 0) is True
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("GE", 1) is False


def test_sensor_reading_is_less_than_method():
    """Testing LT mode of reading_is method"""

    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("LT", -1) is False
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("LT", 0) is False
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("LT", 1) is True


def test_sensor_reading_is_less_than_or_equal_method():
    """Testing LE mode of reading_is method."""

    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("LE", -1) is False
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("LE", 0) is True
    assert BASIC_DAYLIGHT_SENSOR.compare_sensor_reading("LE", 1) is True


def test_random_sensor_reading():
    """Test that the random sensor reading is within the range."""
