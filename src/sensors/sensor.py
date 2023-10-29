"""Module for base class for all sensors."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

from src.sensors.randomize_sensor_data_value import randomize_sensor_data_value
from src.sensors.quantity import QuantityKind


@dataclass
class Sensor:
    """Base class for all sensors.

    This class uses the `randomize_sensor_data_value` function
    to generate random sensor data.
    """

    name: str
    uuid: int

    # The attribute `_kind` is initialized by the `__post_init__` method of the subclass.
    _sensor_kind: QuantityKind = field(init=False, default=QuantityKind.NONE)
    _sensor_last_reading: int = field(init=False)

    # Used to generate random sensor data.
    # Unrelated to the sensor data itself.
    __sensor_random_variables: tuple[int, int, float] = field(
        init=False, default_factory=(lambda: (0, 100, 0.1))
    )

    def __post_init__(self) -> None:
        """Initialize sensor data."""
        self._sensor_last_reading: int = self.__sensor_random_variables[0]

    def update_sensor(self) -> str:
        """Update the sensor data and return a loggable string."""

        range_min, range_max, variation_percentage = self.__sensor_random_variables

        self._sensor_last_reading = randomize_sensor_data_value(
            self._sensor_last_reading,
            range_min,
            range_max,
            variation_percentage,
        )

        return self.get_loggable_string()

    def get_loggable_string(self) -> str:
        """Get a loggable string representing the current state of the sensor."""

        curr_time: datetime = datetime.now(timezone.utc)

        return f"[{curr_time}] {self.name}: current {self._sensor_kind} reading is {self._sensor_last_reading}."

    def get_sensor_kind(self) -> QuantityKind:
        """Get the sensor kind."""
        return self._sensor_kind

    def get_sensor_last_reading(self) -> int:
        """Get the current sensor value."""
        return self._sensor_last_reading

    def compare_sensor_reading(
        self,
        comparison_mode: Literal["EQ", "NE", "LE", "GE", "LT", "GT"],
        target_value: int,
    ) -> bool:
        """Compare the current sensor reading with a target value."""
        curr_reading: int = self._sensor_last_reading

        match comparison_mode:
            case "EQ":
                return curr_reading == target_value

            case "NE":
                return curr_reading != target_value

            case "GT":
                return curr_reading > target_value

            case "GE":
                return curr_reading >= target_value

            case "LT":
                return curr_reading < target_value

            case _:
                return curr_reading <= target_value
