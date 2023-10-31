"""Module for base class for smart devices."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.sensors.quantity import QuantityKind


@dataclass
class Device:
    """Class for smart devices."""

    name: str
    uuid: int

    _device_kind: QuantityKind = field(init=False, default=QuantityKind.NONE)
    _device_value: int = field(init=False, default=0)

    _device_value_range: tuple[int, int] = field(
        init=False,
    )

    def __post_init__(self) -> None:
        self._device_value_range: tuple[int, int] = (0, 100)
        self._device_value = 0

    def get_loggable_string(self) -> str:
        """Return a string representation of the current state of the smart device."""

        curr_time: datetime = datetime.now(timezone.utc)

        return f"[{curr_time}] {self.name}: current {self._device_kind} set to {self._device_value}."

    def get_device_value_range(self) -> tuple[int, int]:
        """Return the range of the smart device."""

        return self._device_value_range

    def get_device_kind(self) -> QuantityKind:
        """Return the kind of the smart device."""

        return self._device_kind

    def get_device_value(self) -> int:
        """Return the current value of the smart device."""

        return self._device_value

    def set_device_value(self, value: int) -> str:
        """Set the current value of the smart device."""

        value_min, value_max = self._device_value_range

        value = min(value, value_max)
        value = max(value, value_min)

        self._device_value = value

        return self.get_loggable_string()
