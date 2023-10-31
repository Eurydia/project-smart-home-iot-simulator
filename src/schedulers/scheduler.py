"""Scheduler that can be used to schedule events and update sensors."""


from dataclasses import dataclass, field
from time import sleep
from typing import Callable

import PySimpleGUI as sg

from src.sensors.sensor import Sensor
from src.devices.device import Device
from src.schedulers.scheduler_logger import SchedulerLogger
from src.schedulers.scheduler_event import SchedulerEvent


def prepare_sensor_status(
    sensor_record: dict[int, Sensor],
) -> str:
    """Prepare the sensor status text."""

    sensor_status_text: str = "\n"

    for _, sensor in sensor_record.items():
        loggable: str = sensor.get_loggable_string()
        sensor_status_text = f"{sensor_status_text}{loggable}\n"

    return sensor_status_text


@dataclass
class Scheduler:
    """Scheduler that can be used to schedule events and update sensors."""

    event_logger: SchedulerLogger
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

    def start_interface(self) -> None:
        """Start the scheduler interface."""

        device_controls: list[list[sg.Element]] = []

        for uuid, device in self._record_devices.items():
            device_controls.append([sg.Text(device.name)])
            device_controls.append(
                [
                    sg.Text(
                        f"{device.get_device_kind()}: {device.get_device_value()}",
                        key=f"device-value-{uuid}",
                    )
                ]
            )
            device_controls.append(
                [
                    sg.Slider(
                        range=device.get_device_value_range(),
                        default_value=device.get_device_value(),
                        key=f"device-control-{uuid}",
                        orientation="horizontal",
                        enable_events=True,
                    )
                ]
            )

        layout = [
            [sg.Text("Smart Home Automation")],
            [sg.Text("Sensor status:")],
            [
                sg.Text(
                    prepare_sensor_status(self._record_sensors),
                    auto_size_text=True,
                    key="sensor-status",
                )
            ],
            *device_controls,
            [sg.Text("Control Status: Manual", key="control-status")],
            [
                sg.Button("Manual", key="control-status-manual"),
                sg.Button("Autopilot", key="control-status-auto"),
            ],
            [sg.Button("cancel")],
        ]

        def dispatch_event() -> None:
            window["sensor-status"].update(
                prepare_sensor_status(self._record_sensors),
            )

            for uuid, devices in self._record_devices.items():
                window[f"device-value-{uuid}"].update(
                    f"{devices.get_device_kind()}: {devices.get_device_value()}"
                )
                window[f"device-control-{uuid}"].update(
                    value=devices.get_device_value(),
                )

        window = sg.Window("Window Title", layout).finalize()

        while True:
            window_data: tuple[str, dict[str, float]] = window.read()

            event: str = window_data[0]
            values: dict[str, float] = window_data[1]

            if event in (sg.WIN_CLOSED, "cancel"):
                break

            if event == "control-status-auto":
                window["control-status"].update("Control Status: Auto")
                window["control-status-auto"].update(disabled=True)
                window.perform_long_operation(
                    lambda: self._start_automatic_schedule(dispatch_event),
                    "scheduler-stopped",
                )
                continue

            if event != "control-status-auto":
                self._runnning = False
                window["control-status"].update("Control Status: Manual")
                window["control-status-auto"].update(disabled=False)

            if event.startswith("device-control-"):
                uuid: int = int(event.removeprefix("device-control-"))
                loggable_text: str = self._record_devices[uuid].set_device_value(
                    int(values[event]),
                )
                self.event_logger.add_log(loggable_text)

            if event == "control-status-manual":
                self._update_sensors()
                self._evaluate_events()

                window["sensor-status"].update(
                    prepare_sensor_status(self._record_sensors),
                )

            for uuid, devices in self._record_devices.items():
                window[f"device-value-{uuid}"].update(
                    f"{devices.get_device_kind()}: {devices.get_device_value()}",
                )
                window[f"device-control-{uuid}"].update(
                    value=devices.get_device_value(),
                )

        window.close()

    def _start_automatic_schedule(
        self,
        dispatch_event: Callable[[], None],
        debug: bool = False,
    ) -> None:
        """Start the scheduler.

        Each run, the sensors are updated and the events are checked.
        If an event should be triggered,
        the actions of the event are executed and logged.
        """

        # If the scheduler is already running, stop it.
        if self._runnning:
            self._runnning = False
            return

        self._runnning = True

        while self._runnning:
            self._update_sensors()
            self._evaluate_events()

            dispatch_event()

            sleep(self.update_interval_sec)

            if debug:
                break

    def _update_sensors(self) -> None:
        """Update registered sensors."""

        for _, sensor in self._record_sensors.items():
            sensor_log: str = sensor.update_sensor()

            self.event_logger.add_log(sensor_log)

    def _evaluate_events(self) -> None:
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
