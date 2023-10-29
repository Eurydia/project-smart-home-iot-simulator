"""Module for smart lights."""

from dataclasses import dataclass


from src.devices.device import Device
from src.sensors.quantity import QuantityKind


@dataclass
class SmartLight(Device):
    """Class for smart lights."""

    def __post_init__(self) -> None:
        super().__post_init__()

        # self._device_value_range = (0, 100)
        self._device_kind = QuantityKind.BRIGHTNESS
