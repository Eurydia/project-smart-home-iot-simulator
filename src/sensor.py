"""Sensor class and related functions.


The randomize_sensor_data_value function is used only by the Sensor class.

I want to make it explicitly clear that randomize_sensor_data_value
is not part of the public API of the sensor module.
It is only used by the Sensor class, and it is not meant to be used
by the user of the sensor module.
"""


from datetime import datetime, timezone
from typing import Literal
from random import randrange
from math import floor

from src.physical_quantity import PhysicalQuantity


def _randomize_sensor_data_value(
    sensor_reading: int,
    sensor_reading_range: tuple[int, int],
    variation_percentage: float = 0.1,
    step: int = 1,
) -> int:
    """Randomize sensor data based on previous value and variation percentage
    The function `randomize_sensor_data_value` is used only by the `Sensor` class.

    Parameters
    ----------
    sensor_reading : int
        The previous value of the sensor.
    sensor_reading_range : tuple[int, int]
        The range of values that the sensor can measure. (inclusive)
    variation_percentage : float, optional
        The percentage of variation from the previous value, by default 0.1
    step : int, optional
        The step of the range, by default 1

    Returns
    -------
    int
        The randomized sensor reading.
    """

    range_min, range_max = sensor_reading_range

    variant_allowed: int = floor(sensor_reading * variation_percentage) + floor(
        (range_max - range_min) * variation_percentage
    )

    random_min_value: int = max(range_min, sensor_reading - variant_allowed)
    random_max_value: int = min(range_max, sensor_reading + variant_allowed)

    return randrange(random_min_value, random_max_value, step)


class Sensor:
    """Class for sensors.

    Attributes
    ----------
    name : str
        The name of the sensor.
    uuid : int
        The unique identifier of the sensor.
    sensor_kind : PhysicalQuantity
        The physical quantity that the sensor measures.
    sensor_reading_range : tuple[int, int]
        The range of values that the sensor can measure.
    sensor_reading : int
        The current value of the sensor.
    """

    _uuid_tracker: int = 1

    def __init__(
        self,
        name: str,
        sensor_kind: PhysicalQuantity,
        sensor_reading_range: tuple[int, int],
    ) -> None:
        self.name = name
        self.sensor_reading_range = sensor_reading_range

        range_min, _ = self.sensor_reading_range
        self._sensor_reading: int = range_min
        self._sensor_kind = sensor_kind

        self._uuid = self.__class__._uuid_tracker
        self.__class__._uuid_tracker += 1

    def update_sensor_value(self) -> str:
        """Update the sensor reading.
        Return a loggable string representation of the current state of the sensor.ku

        Returns
        -------
        str
            A loggable string representation of the current state of the sensor.
        """

        self._sensor_reading = _randomize_sensor_data_value(
            self._sensor_reading,
            self.sensor_reading_range,
        )

        return self.get_loggable_text()

    def get_loggable_text(self, include_timestamp: bool = True) -> str:
        """Return a loggable string representation of the current state of the sensor.\
        If include_timestamp is True, the timestamp will be in UTC.


        Parameters
        ----------
        include_timestamp : bool, optional
            Whether to include a timestamp in the loggable string, by default True

        Returns
        -------
        str
            The loggable string representation of the current state of the sensor.
        """

        loggable_text: str = f"{self.name}: current {self._sensor_kind} reading is {self._sensor_reading}."

        if not include_timestamp:
            return loggable_text

        timestamp: datetime = datetime.now(timezone.utc)

        return f"[{timestamp}] {loggable_text}"

    @property
    def uuid(self) -> int:
        """Get the unique identifier of the sensor."""

        return self._uuid

    @property
    def sensor_kind(self) -> PhysicalQuantity:
        """Get the physical quantity that the sensor measures."""

        return self._sensor_kind

    @property
    def sensor_reading(self) -> int:
        """Get the current value of the sensor."""

        return self._sensor_reading

    def compare_sensor_reading(
        self,
        mode: Literal["EQ", "NE", "LE", "GE", "LT", "GT"],
        value: int,
    ) -> bool:
        """Compare the current sensor reading to a value.

        Different modes are available:
        - EQ: equal to
        - NE: not equal to
        - LE: less than or equal to
        - GE: greater than or equal to
        - LT: less than
        - GT: greater than

        Parameters
        ----------
        mode : Literal["EQ", "NE", "LE", "GE", "LT", "GT"]
            The comparison mode.
        value : int
            The value to compare to.

        Returns
        -------
        bool
            The result of the comparison.
        """
        curr_reading: int = self._sensor_reading

        match mode:
            case "EQ":
                return curr_reading == value

            case "NE":
                return curr_reading != value

            case "GT":
                return curr_reading > value

            case "GE":
                return curr_reading >= value

            case "LT":
                return curr_reading < value

            case _:
                return curr_reading <= value


BASIC_THERMOMETER = Sensor(
    name="Basic Thermometer",
    sensor_kind=PhysicalQuantity.TEMPERATURE,
    sensor_reading_range=(-20, 75),
)

BASIC_HYGROMETER = Sensor(
    name="Basic Hygrometer",
    sensor_kind=PhysicalQuantity.AIR_HUMIDITY,
    sensor_reading_range=(0, 100),
)

BASIC_DAYLIGHT_SENSOR = Sensor(
    name="Basic Daylight Sensor",
    sensor_kind=PhysicalQuantity.BRIGHTNESS,
    sensor_reading_range=(0, 100),
)

BASIC_MOTION_SENSOR = Sensor(
    name="Basic Motion Sensor",
    sensor_kind=PhysicalQuantity.MOTION,
    sensor_reading_range=(0, 100),
)
