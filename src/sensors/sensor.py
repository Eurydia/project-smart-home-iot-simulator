from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, StrEnum, auto
from random import randrange
from math import floor


class OperationMode(Enum):
    IS_EQUAL = auto()
    IS_NOT_EQUAL = auto()
    IS_GREATER_THAN = auto()
    IS_GREATER_THAN_OR_EQUAL_TO = auto()
    IS_LESS_THAN = auto()
    IS_LESS_THAN_OR_EQUAL_TO = auto()


class SensorDataKind(StrEnum):
    UV_INDEX = "UV_INDEX"
    BRIGHTNESS = "BRIGNTNESS"
    AIR_HUMIDITY = "AIR_HUMIDITY"
    SOIL_HUMIDITY = "SOIL_HUMIDITY"
    RELATIVE_TEMPARATURE = "RELATIVE_TEMPARATURE"
    TEMPERATURE = "TEMPARATURE"


@dataclass
class SensorData:
    sensor_data_kind: SensorDataKind
    value: int


@dataclass
class SensorPayload:
    sender_uuid: int
    sender_name: str
    datetime_utc_aware: datetime
    sensor_data: list[SensorData] = field(default_factory=list)


@dataclass
class Sensor:
    name: str
    uuid: int

    sensor_range_min: int = field(init=False, default=0)
    sensor_range_max: int = field(init=False, default=100)
    sensor_variation_percentage: float = field(init=False, default=0.1)

    _sensor_data: dict[SensorDataKind, SensorData] = field(
        init=False, default_factory=dict
    )

    def _generate_random_sensor_data(
        self,
        previous_value: int,
        step: int = 1,
    ) -> int:
        """By simply calling `randrange` to stimulate real world data, one issue
        that I do not like is how much the data fluctuates.

        For example, at one point the UV index was read at 2,
        then in the next second the UV index jumped to 20, which is absurd.

        The point of this function is to make the simulation more realistic.

        This is done by instead of generate a random value every time.
        The function accepts the previous value along with some permissible variation.

        The parameters `min_value` and `max_value` take precedence over variant.

        Args:
        :param:
            previous_value (int): The previously generated random value.
            variant_percentage (float): Variation allowed from `previous_value`.
            min_value (int, optional): Smallest value allowed. Defaults to 0.
            max_value (int, optional): Largest value allowed. Defaults to 100.
            step (int, optional): _description_. Defaults to 1.

        Returns:
            int: A newly generated random number.
        """
        min_value: int = self.sensor_range_min
        max_value: int = self.sensor_range_max
        variation_percentage: float = self.sensor_variation_percentage

        variant_allowed: int = floor(previous_value * variation_percentage) + floor(
            (max_value - min_value) * variation_percentage
        )

        random_min_value: int = max(min_value, previous_value - variant_allowed)
        random_max_value: int = min(max_value, previous_value + variant_allowed)

        return randrange(random_min_value, random_max_value, step)

    def update_sensor_data(self) -> None:
        for key, data in self._sensor_data.items():
            data.value = self._generate_random_sensor_data(
                data.value,
            )

            self._sensor_data[key] = data

    def get_sensor_payload(self) -> SensorPayload:
        datetime_utc_aware: datetime = datetime.now(timezone.utc)
        return SensorPayload(
            self.uuid,
            self.name,
            datetime_utc_aware,
            self._sensor_data,
        )

    def data_is(
        self,
        sensor_data_kind: SensorDataKind,
        operation_mode: OperationMode,
        target_value: int,
    ) -> bool:
        if sensor_data_kind not in self._sensor_data:
            return False

        sensor_data: SensorData = self._sensor_data[sensor_data_kind]
        sensor_data_value: int = sensor_data.value

        match (operation_mode):
            case OperationMode.IS_EQUAL:
                return sensor_data_value == target_value

            case OperationMode.IS_NOT_EQUAL:
                return sensor_data_value != target_value

            case OperationMode.IS_GREATER_THAN:
                return sensor_data_value > target_value

            case OperationMode.IS_GREATER_THAN_OR_EQUAL_TO:
                return sensor_data_value >= target_value

            case OperationMode.IS_LESS_THAN:
                return sensor_data_value < target_value

            case OperationMode.IS_LESS_THAN_OR_EQUAL_TO:
                return sensor_data_value <= target_value
