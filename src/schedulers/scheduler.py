"""Scheduler that can be used to schedule events and update sensors."""
from dataclasses import dataclass, field
from time import sleep


from src.sensors.sensor import Sensor
from src.devices.device import Device
from src.schedulers.scheduler_logger import SchedulerLogger
from src.schedulers.scheduler_event import SchedulerEvent


@dataclass
class Scheduler:
    """Scheduler that can be used to schedule events and update sensors."""

    event_logger: SchedulerLogger
    sensor_logger: SchedulerLogger
    update_interval_sec: int = field(default=5)

    _runnning: bool = field(
        init=False,
        default=False,
    )

    _scheduler_events: list[SchedulerEvent] = field(
        init=False,
        default_factory=list,
    )
    _record_sensors: dict[int, Sensor] = field(
        init=False,
        default_factory=dict,
    )
    _record_devices: dict[int, Device] = field(
        init=False,
        default_factory=dict,
    )

    def is_running(self) -> bool:
        """Return whether the scheduler is running."""
        return self._runnning

    def stop_schedule(self) -> None:
        """Stop the scheduler."""
        self._runnning = False

    def start_schedule(self, debug: bool = False) -> None:
        """Start the scheduler.

        Each run, the sensors are updated and the events are checked.
        If an event should be triggered,
        the actions of the event are executed and logged.
        """

        # If the scheduler is already running, stop it.
        if self._runnning:
            self.stop_schedule()
            return

        self._runnning = True

        while self._runnning:
            self.update_sensors()
            self.check_events()

            sleep(self.update_interval_sec)

            if debug:
                break

    def update_sensors(self) -> None:
        """Update registered sensors."""

        for _, sensor in self._record_sensors.items():
            sensor_log: str = sensor.update_sensor()

            self.sensor_logger.add_log(sensor_log)

    def check_events(self) -> None:
        """Check the requirements of the events in the scheduler.

        If an event should be triggered,
        the actions of the event are executed and logged.
        """

        for event in self._scheduler_events:
            if not event.should_trigger():
                continue
            event_logs: list[str] = event.trigger_actions()

            for event_log in event_logs:
                self.event_logger.add_log(event_log)

    def get_sensors(self) -> list[Sensor]:
        """Return the registered sensors as a list."""

        return list(self._record_sensors.values())

    def get_devices(self) -> list[Device]:
        """Return the registered smart devices as a list."""

        return list(self._record_devices.values())

    def set_device_value(self, device_uuid: int, value: int) -> str:
        """Set the value of a smart device."""

        loggable_msg: str = self._record_devices[device_uuid].set_device_value(value)

        self.event_logger.add_log(loggable_msg)
        return loggable_msg

    # registry methods
    def register_events(
        self,
        events: list[SchedulerEvent],
    ) -> None:
        """Register events to the scheduler."""

        self._scheduler_events.extend(events)

    def register_sensors(
        self,
        sensors: list[Sensor],
    ) -> None:
        """Register sensors to the scheduler."""

        for sensor in sensors:
            if sensor.uuid in self._record_sensors:
                continue
            self._record_sensors[sensor.uuid] = sensor

    def register_devices(
        self,
        devices: list[Device],
    ) -> None:
        """Register smart devices to the scheduler."""

        for device in devices:
            if device.uuid in self._record_devices:
                continue
            self._record_devices[device.uuid] = device
