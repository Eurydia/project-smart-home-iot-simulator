from dataclasses import dataclass


from src.sensors.sensor import Sensor, SensorData, SensorDataKind


@dataclass
class SunlightSensor(Sensor):
    def __post_init__(self) -> None:
        self._sensor_data: dict[SensorDataKind, SensorData] = {
            SensorDataKind.BRIGHTNESS: SensorData(
                SensorDataKind.BRIGHTNESS,
                self.sensor_range_min,
            )
        }


@dataclass
class UVSensor(Sensor):
    sensor_range_min: int = 0
    sensor_range_max: int = 15
    sensor_variation_percentage: float = 0.2

    def __post_init__(self) -> None:
        self._sensor_data: dict[SensorDataKind, SensorData] = {
            SensorDataKind.UV_INDEX: SensorData(
                SensorDataKind.UV_INDEX,
                self.sensor_range_min,
            )
        }
