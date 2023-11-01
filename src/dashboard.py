from __future__ import annotations

from typing import Callable
from threading import Thread

import tkinter as tk

from src.scheduler import Scheduler
from src.logger import Logger
from src.device import Device
from src.sensor import Sensor


def _prepare_sensor_status(
    window: tk.Tk,
    sensors: list[Sensor],
) -> dict[int, tk.StringVar]:
    record_widgets: dict[int, tk.StringVar] = {}
    for sensor in sensors:
        label_name = tk.Label(window, text=sensor.name)
        label_name.pack()

        label_value_text: tk.StringVar = tk.StringVar()
        label_value_text.set(f"{sensor.sensor_kind}: {sensor.sensor_reading}")
        label_value = tk.Label(
            window,
            textvariable=label_value_text,
        )
        label_value.pack()

        record_widgets[sensor.uuid] = label_value_text

    return record_widgets


def _prepare_device_controls(
    window: tk.Tk,
    devices: list[Device],
) -> dict[int, tuple[tk.StringVar, tk.DoubleVar, tk.Scale]]:
    record_widgets: dict[int, tuple[tk.StringVar, tk.DoubleVar, tk.Scale]] = {}

    for device in devices:
        label_name = tk.Label(window, text=device.name)
        label_name.pack()

        label_value_text: tk.StringVar = tk.StringVar()
        label_value_text.set(f"{device.device_kind}: {device.device_value}")
        label_value = tk.Label(
            window,
            textvariable=label_value_text,
        )
        label_value.pack()

        range_min, range_max = device.device_value_range
        slider_value: tk.DoubleVar = tk.DoubleVar(value=device.device_value)
        slider = tk.Scale(
            window,
            variable=slider_value,
            from_=range_min,
            to=range_max,
            orient=tk.HORIZONTAL,
        )
        slider.pack()

        record_widgets[device.uuid] = (
            label_value_text,
            slider_value,
            slider,
        )

    return record_widgets


class Dashboard(tk.Tk):
    """The dashboard is the main window of the application.

    It is responsible for displaying the sensor readings and device values.
    It also provides the user with the ability to control the devices manually.

    The dashboard is also responsible for starting the autopilot.

    Attributes
    ----------
    scheduler : Scheduler
        The scheduler is responsible for updating the sensors and devices.
    logger : Logger
        The logger is responsible for logging the events.



    """

    def __init__(self, scheduler: Scheduler, logger: Logger) -> None:
        super().__init__()
        self.scheduler: Scheduler = scheduler
        self.logger: Logger = logger

        self.thread: Thread = Thread(
            target=self.scheduler.autopilot,
            args=(self._update_dashboard_widgets,),
            daemon=True,
        )

        self.record_widget_sensor = _prepare_sensor_status(self, scheduler.sensors)
        self.record_widget_device = _prepare_device_controls(self, scheduler.devices)

        for uuid, (_, _, slider) in self.record_widget_device.items():

            def _event_wrapper(
                device_uuid: int,
            ) -> Callable[[tk.Event[tk.Scale]], None]:
                return lambda e: self._on_device_slider_change(
                    device_uuid,
                    e,
                )

            slider.bind("<ButtonRelease-1>", _event_wrapper(uuid))

        self.control_status_text: tk.StringVar = tk.StringVar()
        self.control_status_text.set("Control Status: Manual")
        control_status = tk.Label(
            self,
            textvariable=self.control_status_text,
        )
        control_status.pack()

        self.button_manual_control = tk.Button(
            self,
            text="Manual",
            command=self._on_dashboard_manual_click,
        )
        self.button_manual_control.pack()

        self.button_automatic_control = tk.Button(
            self, text="Autopilot", command=self._on_dashboard_autopilot_click
        )
        self.button_automatic_control.pack()

    def _update_dashboard_widgets(self, loggable_texts: list[str]) -> None:
        self.logger.log_texts(loggable_texts)

        for uuid, label_text in self.record_widget_sensor.items():
            for sensor in self.scheduler.sensors:
                if sensor.uuid != uuid:
                    continue
                label_text.set(f"{sensor.sensor_kind}: {sensor.sensor_reading}")

        for uuid, (label_text, slider_value, _) in self.record_widget_device.items():
            for device in self.scheduler.devices:
                if device.uuid != uuid:
                    continue
                label_text.set(f"{device.device_kind}: {device.device_value}")
                slider_value.set(device.device_value)

    def _disable_autopilot(self) -> None:
        if not self.scheduler.running:
            return

        self.control_status_text.set("Control Status: Manual")
        self.button_automatic_control["state"] = tk.NORMAL

        # self.logger.log_text("Manual control activated.")

        self.scheduler.stop()

    def _on_dashboard_manual_click(self) -> None:
        """Update the sensors and evaluate the events.
        This event updates everything including the sensor reading and device value.
        """

        self._disable_autopilot()
        self.scheduler.manual_update(self._update_dashboard_widgets)

    def _on_device_slider_change(
        self,
        device_uuid: int,
        _: tk.Event[tk.Scale],
    ) -> None:
        """Update the device value when the slider is changed.

        It should not update anything but the device value.
        """

        self._disable_autopilot()

        for uuid, (
            string_label,
            slider_value,
            __,
        ) in self.record_widget_device.items():
            if device_uuid != uuid:
                continue

            for device in self.scheduler.devices:
                if device.uuid != uuid:
                    continue
                loggable_text: str = device.set_device_value(
                    int(slider_value.get()),
                )
                self.logger.log_text(loggable_text)
                string_label.set(f"{device.device_kind}: {slider_value}")

    def _on_dashboard_autopilot_click(self) -> None:
        """This event starts the autopilot and updates the sensors and evaluate the events.

        Similar to the manual update, this event updates everything including the sensor reading and device value.
        But the button is disabled itself to prevent the user from clicking it again.
        """

        # self.scheduler.manual_update(self._update_window)
        self.control_status_text.set("Control Status: Autopilot")
        self.button_automatic_control["state"] = tk.DISABLED

        self.logger.log_text("Autopilot activated.")

        self.scheduler.start()
        self.thread.start()

    def start(self) -> None:
        """Start the dashboard."""

        self.mainloop()
