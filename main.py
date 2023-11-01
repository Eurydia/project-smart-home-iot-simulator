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

from src.scheduler import Scheduler, SchedulerEvent
from src.logger import Logger
from src.physical_quantity import PhysicalQuantity
from src.sensor import Sensor
from src.device import Device
from src.dashboard import Dashboard


def prepare_basic_scheduler() -> Scheduler:
    """Prepare the scheduler."""

    # Prepare sensors
    main_sunlight_sensor: Sensor = Sensor(
        "Main sunlight sensor",
        PhysicalQuantity.BRIGHTNESS,
        (0, 100),
    )
    main_humidity_sensor: Sensor = Sensor(
        "Main humidity sensor",
        PhysicalQuantity.AIR_HUMIDITY,
        (0, 100),
    )
    main_thermometer: Sensor = Sensor(
        "Main thermometer",
        PhysicalQuantity.TEMPERATURE,
        (-20, 75),
    )
    bathroom_motion_sensor: Sensor = Sensor(
        "Bathroom motion sensor",
        PhysicalQuantity.MOTION,
        (0, 100),
    )

    # Prepare actuators
    front_door_light: Device = Device(
        "Front door light",
        PhysicalQuantity.BRIGHTNESS,
        (0, 100),
    )
    bathroom_light: Device = Device(
        "Bathroom light",
        PhysicalQuantity.BRIGHTNESS,
        (0, 100),
    )
    balcony_light: Device = Device(
        "Front door light",
        PhysicalQuantity.BRIGHTNESS,
        (0, 100),
    )
    bed_room_humidifier: Device = Device(
        "Bed room humidifier",
        PhysicalQuantity.AIR_HUMIDITY,
        (0, 100),
    )
    primary_air_conditioner: Device = Device(
        "Primary air conditioner",
        PhysicalQuantity.TEMPERATURE,
        (18, 30),
    )

    # Prepare events

    # turn on lights when it is dark (brightness <= 20)
    turn_on_light_when_dark: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: main_sunlight_sensor.compare_sensor_reading("LE", 20),
        ],
        actions=[
            lambda: front_door_light.set_device_value(75),
            lambda: balcony_light.set_device_value(75),
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
            (lambda: balcony_light.set_device_value(25)),
        ],
    )
    turn_on_bathroom_light_when_motion_detected: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: bathroom_motion_sensor.compare_sensor_reading("GT", 80),
        ],
        actions=[
            (lambda: bathroom_light.set_device_value(100)),
        ],
    )
    turn_off_bathroom_light_after_use: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: bathroom_motion_sensor.compare_sensor_reading("LE", 80),
        ],
        actions=[
            (lambda: bathroom_light.set_device_value(0)),
        ],
    )

    # turn off lights when it is bright (brightness > 40)
    turn_off_front_light_when_bright: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: main_sunlight_sensor.compare_sensor_reading("GT", 40),
        ],
        actions=[
            (lambda: front_door_light.set_device_value(0)),
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
        # bathroom light events
        turn_on_bathroom_light_when_motion_detected,
        turn_off_bathroom_light_after_use,
        # humidifier events
        activate_humidifier_when_humidity_low,
        deactivate_humidifier_when_humidity_high,
        # air conditioner events
        lower_temp_when_hot,
        raise_temp_when_cold,
    ]

    scheduler: Scheduler = Scheduler()

    # register sensors and events
    scheduler.register_sensors(
        [
            main_sunlight_sensor,
            main_humidity_sensor,
            main_thermometer,
            bathroom_motion_sensor,
        ]
    )
    scheduler.register_devices(
        [
            front_door_light,
            bathroom_light,
            balcony_light,
            bed_room_humidifier,
            primary_air_conditioner,
        ]
    )
    scheduler.register_events(scheduler_events)

    return scheduler


def main() -> None:
    basic_scheduler: Scheduler = prepare_basic_scheduler()
    # basic_scheduler.start_interface()
    # prepare scheduler
    with open(
        "logs/event_logs.txt",
        "w",
        encoding="utf-8",
    ) as event_log_file:
        basic_logger: Logger = Logger(
            event_log_file,
            log_function=print,
        )
        my_dashboard = Dashboard(basic_scheduler, basic_logger)
        my_dashboard.start()


if __name__ == "__main__":
    main()
