from __future__ import absolute_import

import PySimpleGUI as sg


from src.sensors.sensor import SensorDataKind, OperationMode
from src.sensors.sensor_photometric import SunlightSensor
from src.schedulers.scheduler import Scheduler
from src.smart_devices.smart_device_light import SmartDeviceLight
from src.event import Event


def main() -> None:
    sensor_daylight: SunlightSensor = SunlightSensor(
        "Daylight Sensor",
        123,
    )
    smart_light: SmartDeviceLight = SmartDeviceLight(
        "Front door light #1",
        124,
    )

    event: Event = Event(
        name=f"Turn on {smart_light.name} when {sensor_daylight.name}'s value is <= 20",
        requirements=[
            lambda: sensor_daylight.data_is(
                SensorDataKind.BRIGHTNESS, OperationMode.IS_LESS_THAN, 20
            ),
            lambda: not smart_light.running,
        ],
        act=(lambda: smart_light.set_brightness_level(50)),
    )

    scheduler: Scheduler = Scheduler(update_interval_sec=2)
    scheduler.register_sensor(sensor_daylight)
    scheduler.register_event(event)

    layout = [
        [sg.Text("Some text on Row 1")],
        [sg.Text("Enter something on Row 2"), sg.InputText()],
        [sg.Button("Ok"), sg.Button("Cancel"), sg.Button("auto")],
    ]

    window = sg.Window("Window Title", layout)
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event in ("auto"):
            if not scheduler.runnning:
                window.perform_long_operation(
                    scheduler.start_schedule, "scheduler stopped"
                )
                continue
            scheduler.stop_schedule()

    window.close()


if __name__ == "__main__":
    main()
