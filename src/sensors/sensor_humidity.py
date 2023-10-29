"""Module for sensors that measure humidity."""

from dataclasses import dataclass

from src.sensors.sensor import Sensor
from src.sensors.quantity import QuantityKind


@dataclass
class AirHumiditySensor(Sensor):
    """A sensor that measures the air humidity."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._sensor_kind: QuantityKind = QuantityKind.AIR_HUMIDITY


# @dataclass
# class SoilHumiditySensor(Sensor):
#     """A sensor that measures the soil humidity."""

#     def __post_init__(self) -> None:
#         super().__post_init__()
#         self._sensor_kind: QuantityKind = QuantityKind.SOIL_HUMIDITY
