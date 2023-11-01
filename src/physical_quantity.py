"""Physical quantity enum.

This module can be even more complete
if it contains the units of measurement for each physical quantity.

But for the sake of simplicity, it is not included.
"""

from enum import StrEnum


class PhysicalQuantity(StrEnum):
    """Measurement kind enum."""

    NONE = "NONE"
    UV_INDEX = "UV_INDEX (1-11)"
    BRIGHTNESS = "BRIGHTNESS (%)"
    AIR_HUMIDITY = "AIR_HUMIDITY (%)"
    SOIL_HUMIDITY = "SOIL_HUMIDITY (%)"
    RELATIVE_TEMPARATURE = "RELATIVE_TEMPARATURE (%)"
    TEMPERATURE = "TEMPARATURE (Degrees Celsius)"
    MOTION = "MOTION (%)"
