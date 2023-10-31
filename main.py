"""This is a basic example of how to use the scheduler to
automate a smart home setup.

The setup consists of
- 3 smart lights,
- 1 humidifier,
- 1 air conditioner,
- 1 sunlight sensor,
- 1 humidity sensor and
- 1 temperature sensor.


The smart lights are turned on when it is dark and turned off when it is bright.
Additionally, the lights are dimmed when it is not dark fully dark.

The humidifier is turned on when the humidity is low and
turned off when the humidity is high.

The air conditioner is turned on when the temperature is high and
turned off when the temperature is low.

"""

from src.schedulers.scheduler import Scheduler
from src.schedulers.scheduler_event import SchedulerEvent
from src.schedulers.scheduler_logger import SchedulerLogger

from src.sensors.sensor_photometric import SunlightSensor
from src.sensors.sensor_humidity import AirHumiditySensor
from src.sensors.sensor_temperature import TemperatureSensor

from src.devices.device_light import SmartLight
from src.devices.device_humidifier import SmartHumidifier
from src.devices.device_air_conditioner import Airconditioner


def prepare_basic_scheduler() -> Scheduler:
    """Prepare the scheduler."""

    # prepare sensors and smart devices
    main_sunlight_sensor: SunlightSensor = SunlightSensor(
        "Main sunlight sensor",
        100,
    )
    main_humidity_sensor: AirHumiditySensor = AirHumiditySensor(
        "Main humidity sensor",
        101,
    )
    main_thermometer: TemperatureSensor = TemperatureSensor(
        "Main thermometer",
        102,
    )

    front_door_light: SmartLight = SmartLight(
        "Front door light",
        9024,
    )
    back_door_light: SmartLight = SmartLight(
        "Back door light",
        9025,
    )
    balcony_light: SmartLight = SmartLight(
        "Balcony light",
        9026,
    )

    bed_room_humidifier: SmartHumidifier = SmartHumidifier(
        "Bed room humidifier",
        9027,
    )

    primary_air_conditioner: Airconditioner = Airconditioner(
        "Primary air conditioner",
        9028,
    )

    # Prepare scheduler events
    # turn on lights when it is dark (brightness <= 20)
    turn_on_light_when_dark: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: main_sunlight_sensor.compare_sensor_reading("LE", 20),
        ],
        actions=[
            (lambda: front_door_light.set_device_value(75)),
            (lambda: back_door_light.set_device_value(75)),
            (lambda: balcony_light.set_device_value(75)),
        ],
    )
    # dim lights when it is not dark ( 20 < brightness <= 40)
    dim_light_when_not_dark: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: main_sunlight_sensor.compare_sensor_reading("GT", 20),
            lambda: main_sunlight_sensor.compare_sensor_reading("LE", 40),
        ],
        actions=[
            (lambda: front_door_light.set_device_value(25)),
            (lambda: back_door_light.set_device_value(25)),
            (lambda: balcony_light.set_device_value(25)),
        ],
    )
    # turn off lights when it is bright (brightness > 40)
    turn_off_front_light_when_bright: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: main_sunlight_sensor.compare_sensor_reading("GT", 40),
        ],
        actions=[
            (lambda: front_door_light.set_device_value(0)),
            (lambda: back_door_light.set_device_value(0)),
            (lambda: balcony_light.set_device_value(0)),
        ],
    )
    # activate humidifier when humidity is low (humidity <= 40)
    activate_humidifier_when_humidity_low: SchedulerEvent = SchedulerEvent(
        requirements=[
            (lambda: main_humidity_sensor.compare_sensor_reading("LE", 40)),
        ],
        actions=[
            (lambda: bed_room_humidifier.set_device_value(100)),
        ],
    )

    # deactivate humidifier when humidity is high (humidity > 60)
    deactivate_humidifier_when_humidity_high: SchedulerEvent = SchedulerEvent(
        requirements=[
            (lambda: main_humidity_sensor.compare_sensor_reading("GT", 60)),
        ],
        actions=[
            (lambda: bed_room_humidifier.set_device_value(0)),
        ],
    )

    # lower temperature when hot (temperature > 30)
    lower_temp_when_hot: SchedulerEvent = SchedulerEvent(
        requirements=[
            (lambda: main_thermometer.compare_sensor_reading("GT", 30)),
        ],
        actions=[
            (lambda: primary_air_conditioner.set_device_value(22)),
        ],
    )
    # raise temperature when cold (temperature < 20)
    raise_temp_when_cold: SchedulerEvent = SchedulerEvent(
        requirements=[
            (lambda: main_thermometer.compare_sensor_reading("LT", 20)),
        ],
        actions=[
            (lambda: primary_air_conditioner.set_device_value(20)),
        ],
    )

    scheduler_events: list[SchedulerEvent] = [
        # smart light events
        turn_on_light_when_dark,
        dim_light_when_not_dark,
        turn_off_front_light_when_bright,
        # humidifier events
        activate_humidifier_when_humidity_low,
        deactivate_humidifier_when_humidity_high,
        # air conditioner events
        lower_temp_when_hot,
        raise_temp_when_cold,
    ]

    # prepare scheduler
    with open(
        "logs/event_logs.txt",
        "w",
        encoding="utf-8",
    ) as event_log_file:
        event_logger: SchedulerLogger = SchedulerLogger(
            event_log_file,
            log_function=print,
        )

    scheduler: Scheduler = Scheduler(event_logger, 2)

    # register sensors and events
    scheduler.register_sensors(
        [
            main_sunlight_sensor,
            main_humidity_sensor,
            main_thermometer,
        ]
    )
    scheduler.register_devices(
        [
            front_door_light,
            back_door_light,
            balcony_light,
            bed_room_humidifier,
            primary_air_conditioner,
        ]
    )
    scheduler.register_events(scheduler_events)

    return scheduler


def main() -> None:
    basic_scheduler: Scheduler = prepare_basic_scheduler()
    basic_scheduler.start_interface()


if __name__ == "__main__":
    main()
