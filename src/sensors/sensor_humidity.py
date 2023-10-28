from dataclasses import dataclass

from src.sensors.sensor import Sensor, SensorData, SensorDataKind


@dataclass
class AirHumiditySensor(Sensor):
    def __post_init__(self):
        self._sensor_data: dict[SensorDataKind, SensorData] = {
            SensorDataKind.AIR_HUMIDITY: SensorData(
                SensorDataKind.AIR_HUMIDITY,
                self.sensor_range_min,
            )
        }


@dataclass
class SoilHumiditySensor(Sensor):
    def __post_init__(self):
        self._sensor_data: dict[SensorDataKind, SensorData] = {
            SensorDataKind.SOIL_HUMIDITY: SensorData(
                SensorDataKind.SOIL_HUMIDITY,
                self.sensor_range_min,
            )
        }
