"""Module for base class for smart devices."""

from datetime import datetime, timezone

from src.physical_quantity import PhysicalQuantity


class Device:
    """Class for smart devices.

    Attributes
    ----------
    name : str
        The name of the smart device.
    uuid : int
        The unique identifier of the smart device.
    device_kind : QuantityKind
        The physical quantity that the smart device interacts with.
    device_value_range : tuple[int, int]
        The range of values that the smart device can take.
    device_value : int
        The current value of the smart device.
    """

    _uuid_tracker: int = 100001

    def __init__(
        self,
        name: str,
        device_kind: PhysicalQuantity,
        device_value_range: tuple[int, int],
    ) -> None:
        self.name = name
        self._device_kind = device_kind
        self._device_value_range = device_value_range

        range_min, _ = self._device_value_range
        self._device_value = range_min

        self._uuid = self.__class__._uuid_tracker
        self.__class__._uuid_tracker += 1

    def get_loggable_text(self, include_timestamp: bool = True) -> str:
        """Return a string representation of the current state of the smart device."""

        loggable_text: str = (
            f"{self.name}: current {self._device_kind} set to {self._device_value}."
        )

        if not include_timestamp:
            return loggable_text

        timestamp: datetime = datetime.now(timezone.utc)

        return f"[{timestamp}] {loggable_text}"

    @property
    def uuid(self) -> int:
        """Get the unique identifier of the smart device."""

        return self._uuid

    @property
    def device_value_range(self) -> tuple[int, int]:
        """Return the range of the smart device."""

        return self._device_value_range

    @property
    def device_kind(self) -> PhysicalQuantity:
        """Return the physical quantity that the smart device interacts with."""

        return self._device_kind

    @property
    def device_value(self) -> int:
        """Return the current value of the smart device."""

        return self._device_value

    def set_device_value(self, value: int) -> str:
        """Set the current value of the smart device.

        If the new value is outside the range of the smart device,
        the value is set to the closest bound of the range.

        Parameters
        ----------
        value : int
            The new value of the smart device.

        Returns
        -------
        str
            A loggable string representation of the current state of the smart device.
        """

        range_min, range_max = self._device_value_range

        value = min(value, range_max)
        value = max(value, range_min)

        self._device_value = value

        return self.get_loggable_text()


BASIC_SMART_LIGHT = Device(
    "Basic smart light",
    PhysicalQuantity.BRIGHTNESS,
    (0, 100),
)

BASIC_SMART_HUMIDIFIER = Device(
    "Basic smart humidifier",
    PhysicalQuantity.AIR_HUMIDITY,
    (0, 100),
)

BASIC_SMART_AIR_CONDITIONER = Device(
    "Basic smart air conditioner",
    PhysicalQuantity.TEMPERATURE,
    (18, 30),
)
