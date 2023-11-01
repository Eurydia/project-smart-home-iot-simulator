"""Scheduler that can be used to schedule events and update sensors."""


from time import sleep
from typing import Callable

from src.sensor import Sensor
from src.device import Device


class SchedulerEvent:
    """Scheduler event that can be triggered by a set of requirements and actions."""

    def __init__(
        self,
        *,
        actions: list[Callable[[], str]],
        requirements: list[Callable[[], bool]],
    ) -> None:
        self.__actions = actions
        self.__requirements = requirements

    def should_trigger(self) -> bool:
        """Check if all requirements are met."""

        return all(req() for req in self.__requirements)

    def trigger_actions(self) -> list[str]:
        """Trigger all actions and return the log."""

        return [action() for action in self.__actions]


class Scheduler:
    """Scheduler that can be used to schedule events and update sensors."""

    def __init__(self, *, update_interval_sec: int = 5) -> None:
        self.update_interval_sec = update_interval_sec

        self._running: bool = False

        self._scheduler_events: list[SchedulerEvent] = []
        self._record_sensors: dict[int, Sensor] = {}
        self._record_devices: dict[int, Device] = {}

    def manual_update(
        self,
        dispatch_event: Callable[[list[str]], None],
    ) -> None:
        """Manually update the sensors and evaluate the events."""

        sensor_logs: list[str] = self.__update_sensors()
        event_logs: list[str] = self.__evaluate_events()

        dispatch_event(sensor_logs + event_logs)

    def stop(self) -> None:
        """Stop the scheduler."""

        self._running = False

    def start(self) -> None:
        self._running = True

    def autopilot(
        self,
        dispatch_event: Callable[[list[str]], None],
        debug: bool = False,
    ) -> None:
        """Start the scheduler.

        Each run, the sensors are updated and the events are checked.
        If an event should be triggered,
        the actions of the event are executed and logged.
        """

        while self._running:
            sensor_logs: list[str] = self.__update_sensors()
            event_logs: list[str] = self.__evaluate_events()

            dispatch_event(sensor_logs + event_logs)

            sleep(self.update_interval_sec)

            if debug:
                break

    def __update_sensors(self) -> list[str]:
        """Update registered sensors."""

        loggable_texts: list[str] = []
        for _, sensor in self._record_sensors.items():
            loggable_text: str = sensor.update_sensor_value()
            loggable_texts.append(loggable_text)

        return loggable_texts

    def __evaluate_events(self) -> list[str]:
        """Check the requirements of the events in the scheduler.

        If an event should be triggered,
        the actions of the event are executed and logged.
        """
        event_logs: list[str] = []
        for event in self._scheduler_events:
            if not event.should_trigger():
                continue
            event_logs.extend(event.trigger_actions())

        return event_logs

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
            uuid: int = sensor.uuid
            if uuid in self._record_sensors:
                continue
            self._record_sensors[uuid] = sensor

    def register_devices(
        self,
        devices: list[Device],
    ) -> None:
        """Register smart devices to the scheduler."""

        for device in devices:
            uuid: int = device.uuid
            if uuid in self._record_devices:
                continue
            self._record_devices[uuid] = device

    @property
    def devices(self) -> list[Device]:
        """Return the registered smart devices."""

        return list(self._record_devices.values())

    @property
    def sensors(self) -> list[Sensor]:
        """Return the registered smart devices."""

        return list(self._record_sensors.values())

    @property
    def running(self) -> bool:
        """Return the running state of the scheduler."""

        return self._running
