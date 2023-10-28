from dataclasses import dataclass, field
from time import sleep


from src.sensors.sensor import Sensor
from src.smart_devices.smart_device import SmartDevice
from src.event import Event


@dataclass
class Scheduler:
    runnning: bool = field(default=False)
    update_interval_sec: int = field(default=5)

    record_sensors: dict[int, Sensor] = field(init=False, default_factory=dict)
    record_smart_devices: dict[int, SmartDevice] = field(
        init=False, default_factory=dict
    )
    events: list[Event] = field(init=False, default_factory=list)

    def stop_schedule(self):
        self.runnning = False

    def start_schedule(self) -> None:
        self.runnning = True

        while self.runnning:
            self.update_sensors()

            for event in self.events:
                if not event.should_trigger():
                    continue

                log: str = event.act()
                print(log)

            sleep(self.update_interval_sec)

    def update_sensors(self):
        for _, sensor in self.record_sensors.items():
            sensor.update_sensor_data()

    # registry methods
    def register_event(self, new_event: Event) -> int:
        self.events.append(new_event)
        return len(self.events)

    def register_sensor(self, new_sensor: Sensor) -> bool:
        if new_sensor.uuid in self.record_sensors:
            return False

        self.record_sensors[new_sensor.uuid] = new_sensor
        return True

    def register_smart_device(self, new_smart_device: SmartDevice) -> int:
        if new_smart_device.uuid in self.record_smart_devices:
            return False

        self.record_sensors[new_smart_device.uuid] = new_smart_device
        return True
