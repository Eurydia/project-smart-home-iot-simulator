"""Module for sensors that measure temperature."""

from dataclasses import dataclass

from src.sensors.sensor import Sensor
from src.sensors.quantity import QuantityKind


@dataclass
class TemperatureSensor(Sensor):
    """A sensor that measures the temperature."""

    def __post_init__(self):
        super().__post_init__()
        self._sensor_kind: QuantityKind = QuantityKind.TEMPERATURE
