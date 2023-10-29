"""Module for thermostat/smart airconditioner."""

from dataclasses import dataclass


from src.devices.device import Device
from src.sensors.quantity import QuantityKind


@dataclass
class Airconditioner(Device):
    """Class for thermostat/smart airconditioner."""

    def __post_init__(self) -> None:
        super().__post_init__()
        self._device_value_range = (15, 35)

        self._device_value = 20
        self._device_kind = QuantityKind.TEMPERATURE
