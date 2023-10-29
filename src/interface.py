import PySimpleGUI as sg


from src.schedulers.scheduler import Scheduler


def prepare_status_message(loggable_messages: list[str]) -> str:
    """Prepare the device status message."""
    return "\n".join(loggable_messages)


def prepare_device_controls(scheduler: Scheduler) -> list[list[sg.Element]]:
    """Prepare the device controls."""

    controls: list[list[sg.Element]] = []

    for device in scheduler.get_devices():
        controls.append([sg.Text(device.name)])
        controls.append(
            [
                sg.Text(
                    f"{device.get_device_kind()}: {device.get_device_value()}",
                    key=f"device-value-{device.uuid}",
                )
            ]
        )
        controls.append(
            [
                sg.Slider(
                    range=device.get_device_value_range(),
                    default_value=device.get_device_value(),
                    key=f"device-control-{device.uuid}",
                    orientation="horizontal",
                )
            ]
        )

    return controls


def start_interface(scheduler: Scheduler) -> None:
    layout = [
        [sg.Text("Smart Home Automation")],
        [sg.Text("Sensor status:")],
        [
            sg.Text(
                prepare_status_message(
                    [s.get_loggable_string() for s in scheduler.get_sensors()]
                ),
                auto_size_text=True,
                key="sensor-status",
            )
        ],
        *prepare_device_controls(scheduler),
        [sg.Text("Control Status: Manual", key="control-status")],
        [
            sg.Button("Manual", key="control-status-manual"),
            sg.Button("Autopilot", key="control-status-auto"),
        ],
        [sg.Button("cancel")],
    ]

    window = sg.Window("Window Title", layout)

    while True:
        event, value = window.read()

        if event in (sg.WIN_CLOSED, "cancel"):
            break

        window["sensor-status"].update(
            prepare_status_message(
                [s.get_loggable_string() for s in scheduler.get_sensors()]
            ),
        )

        if event != "control-status-auto":
            scheduler.stop_schedule()
            window["control-status"].update("Control Status: Manual")
            window["control-status-auto"].update(disabled=False)

        if event == "control-status-auto":
            if scheduler.is_running():
                scheduler.stop_schedule()
                continue

            window["control-status"].update("Control Status: Auto")
            window["control-status-auto"].update(disabled=True)
            window.perform_long_operation(
                scheduler.start_schedule,
                "scheduler-stopped",
            )

        if event == "control-status-manual":
            scheduler.update_sensors()
            scheduler.check_events()
            continue

        if event.startswith("device-control-"):
            device_uuid = int(event.removeprefix("device-control-"))
            scheduler.set_device_value(device_uuid, value)
            # window[f"device-value-{device_uuid}"].update("")

    window.close()
