"""Module for sensors that measure motion."""

from dataclasses import dataclass

from src.sensors.sensor import Sensor
from src.sensors.quantity import QuantityKind


@dataclass
class MotionSensor(Sensor):
    """A sensor that measures the amount of motion."""

    def __post_init__(self) -> None:
        # super().__post_init__()
        self.__sensor_random_variables: tuple[int, int, float] = (0, 100, 0.2)

        self._sensor_last_reading: int = self.__sensor_random_variables[0]
        self._sensor_kind: QuantityKind = QuantityKind.MOTION
