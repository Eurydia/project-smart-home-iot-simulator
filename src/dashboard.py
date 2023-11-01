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
        sensor_reading_label_text: tk.StringVar = tk.StringVar(
            value=sensor.get_loggable_text(False),
        )
        sensor_reading_label = tk.Label(
            window,
            textvariable=sensor_reading_label_text,
        )
        sensor_reading_label.pack()

        record_widgets[sensor.uuid] = sensor_reading_label_text

    return record_widgets


def _prepare_device_controls(
    window: tk.Tk,
    devices: list[Device],
) -> dict[int, tuple[tk.StringVar, tk.DoubleVar, tk.Scale]]:
    record_widgets: dict[int, tuple[tk.StringVar, tk.DoubleVar, tk.Scale]] = {}

    for device in devices:
        device_value_label_text = tk.StringVar(
            value=device.get_loggable_text(False),
        )
        device_value_label = tk.Label(
            window,
            textvariable=device_value_label_text,
        )
        device_value_label.pack()

        range_min, range_max = device.device_value_range

        device_slider_value = tk.DoubleVar(
            value=device.device_value,
        )
        device_slider = tk.Scale(
            window,
            variable=device_slider_value,
            from_=range_min,
            to=range_max,
            orient=tk.HORIZONTAL,
        )
        device_slider.pack()

        record_widgets[device.uuid] = (
            device_value_label_text,
            device_slider_value,
            device_slider,
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

        # Prepare the thread for autopilot mode.
        # We can also control the thread from the dashboard
        # by calling start/stop method of the scheduler.
        self.__thread: Thread = Thread(
            target=self.scheduler.autopilot,
            args=(self.__event_update_all_dashboard_widgets,),
            daemon=True,
        )

        # Prepare and keep track of the widgets so that we can update them later.
        # We only need to update labels for sensors.
        # But for devices, we need to update the slider and the label
        self.__record_widget_sensor = _prepare_sensor_status(self, scheduler.sensors)
        self.__record_widget_device = _prepare_device_controls(self, scheduler.devices)

        # Bind the slider event to the slider widget
        for uuid, (_, _, slider) in self.__record_widget_device.items():
            # Defining a function inside a loop is not a good idea.
            # But we need to pass the uuid to the function.

            def _event_wrapper(
                device_uuid: int,
            ) -> Callable[[tk.Event[tk.Scale]], None]:
                return lambda e: self.__event_slider_change(
                    device_uuid,
                    e,
                )

            slider.bind("<ButtonRelease-1>", _event_wrapper(uuid))

        # Prepare the dashboard control buttons and a label.
        # The label is used to display the current control status.
        # The buttons are used to switch between manual and autopilot mode.
        self.__control_status_text: tk.StringVar = tk.StringVar()
        self.__control_status_text.set("Control Status: Manual")
        control_status = tk.Label(
            self,
            textvariable=self.__control_status_text,
        )
        control_status.pack()

        self.__button_manual_control = tk.Button(
            self,
            text="Manual",
            command=self.__event_dashboard_manual_update,
        )
        self.__button_manual_control.pack()

        self.__button_automatic_control = tk.Button(
            self,
            text="Autopilot",
            command=self.__event_dashboard_autopilot,
        )
        self.__button_automatic_control.pack()

    def __event_update_all_dashboard_widgets(
        self,
        loggable_texts: list[str],
    ) -> None:
        """Update the sensors and evaluate the events.

        Also update the dashboard display to reflect the changes.

        This event is fired when the dashboard is manually updated in manual mode.
        In autopilot mode, this event is fired by the autopilot thread
        after the sensors and devices are updated.
        """

        self.logger.log_texts(loggable_texts)

        for uuid, label_text in self.__record_widget_sensor.items():
            for sensor in self.scheduler.sensors:
                if sensor.uuid != uuid:
                    continue
                label_text.set(sensor.get_loggable_text(False))

        for uuid, item in self.__record_widget_device.items():
            (label_text, slider_value, _) = item

            for device in self.scheduler.devices:
                if device.uuid != uuid:
                    continue
                label_text.set(device.get_loggable_text(False))
                slider_value.set(device.device_value)

    def __event_disable_autopilot(self) -> None:
        """Disable the autopilot and enable the manual control.

        This event is fired when the user clicks the manual control button
        or changes the device value using the slider.

        The idea is to override the autopilot mode and switch to manual mode
        when the user resumes the control.
        """

        if not self.scheduler.running:
            return

        self.__control_status_text.set("Control Status: Manual")
        self.__button_automatic_control["state"] = tk.NORMAL

        # self.logger.log_text("Manual control activated.")

        self.scheduler.stop()

    def __event_dashboard_manual_update(self) -> None:
        """Update the sensors and evaluate the events manually.
        This event fires three events:
        1. fires the __event_disable_autopilot event to disable the autopilot.
        2. trigger the scheduler to update the sensors and evaluate the events.
        3. fires the __event_update_all_dashboard_widgets event to update the dashboard display.
        """

        self.__event_disable_autopilot()
        self.scheduler.manual_update(self.__event_update_all_dashboard_widgets)

    def __event_slider_change(
        self,
        device_uuid: int,
        _: tk.Event[tk.Scale],
    ) -> None:
        """Update the device value when the slider is changed.

        This event fires two events:
        1. fires the __event_disable_autopilot event to disable the autopilot.
        2. update the device value.

        So this event only updates the device value.
        It does not cause the dashboard to update other widgets.
        """

        self.__event_disable_autopilot()

        for uuid, (
            string_label,
            slider_value,
            __,
        ) in self.__record_widget_device.items():
            if device_uuid != uuid:
                continue

            for device in self.scheduler.devices:
                if device.uuid != uuid:
                    continue
                loggable_text: str = device.set_device_value(
                    int(slider_value.get()),
                )
                self.logger.log_text(loggable_text)
                string_label.set(device.get_loggable_text(False))

    def __event_dashboard_autopilot(self) -> None:
        """Start the autopilot mode.

        This event signals the autopilot thread to start.
        And begin the autopilot mode.
        """

        # self.scheduler.manual_update(self._update_window)
        self.__control_status_text.set("Control Status: Autopilot")
        self.__button_automatic_control["state"] = tk.DISABLED

        self.logger.log_text("Autopilot activated.")

        self.scheduler.start()

        if self.__thread.is_alive():
            return
        self.__thread.start()

    def start(self) -> None:
        """Start the dashboard."""

        self.mainloop()
