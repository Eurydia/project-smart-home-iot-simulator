"""Module for photometric sensors."""
from dataclasses import dataclass


from src.sensors.sensor import Sensor
from src.sensors.quantity import QuantityKind


@dataclass
class SunlightSensor(Sensor):
    """A sensor that measures the amount of sunlight."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._sensor_kind: QuantityKind = QuantityKind.BRIGHTNESS


# @dataclass
# class UVSensor(Sensor):
#     """A sensor that measures the amount of UV light."""

#     def __post_init__(self) -> None:
#         # super().__post_init__()

#         self.__sensor_random_variables: tuple[int, int, float] = (0, 11, 0.2)

#         self._sensor_kind: QuantityKind = QuantityKind.UV_INDEX
#         self._sensor_last_reading: int = self.__sensor_random_variables[0]
