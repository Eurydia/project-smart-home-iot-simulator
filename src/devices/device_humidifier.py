"""Module for smart humidifiers."""

from dataclasses import dataclass


from src.devices.device import Device
from src.sensors.quantity import QuantityKind


@dataclass
class SmartHumidifier(Device):
    """Class for smart humidifiers."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._device_value_range = (20, 70)

        self._device_value = 50
        self._device_kind = QuantityKind.AIR_HUMIDITY
