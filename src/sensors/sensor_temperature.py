from dataclasses import dataclass

from src.sensors.sensor import (
    Sensor,
    SensorData,
    SensorDataKind,
)


@dataclass
class RelativeTemperatureSensor(Sensor):
    def __post_init__(self):
        self._sensor_data: dict[SensorDataKind, SensorData] = {
            SensorDataKind.RELATIVE_TEMPARATURE: SensorData(
                SensorDataKind.RELATIVE_TEMPARATURE,
                self.sensor_range_min,
            )
        }


@dataclass
class TemperatureSensor(Sensor):
    def __post_init__(self):
        self._sensor_data: dict[SensorDataKind, SensorData] = {
            SensorDataKind.TEMPERATURE: SensorData(
                SensorDataKind.TEMPERATURE,
                self.sensor_range_min,
            )
        }
