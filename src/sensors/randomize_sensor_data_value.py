"""Randomize sensor data based on previous value and variation percentage
The function `randomize_sensor_data_value` is used only by the `Sensor` class.
"""

from random import randrange
from math import floor


def randomize_sensor_data_value(
    previous_value: int,
    range_min: int,
    range_max: int,
    variation_percentage: float,
    step: int = 1,
) -> int:
    """Generate random sensor data based on previous value and variation percentage"""

    variant_allowed: int = floor(previous_value * variation_percentage) + floor(
        (range_max - range_min) * variation_percentage
    )

    random_min_value: int = max(range_min, previous_value - variant_allowed)
    random_max_value: int = min(range_max, previous_value + variant_allowed)

    return randrange(random_min_value, random_max_value, step)
