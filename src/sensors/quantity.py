from enum import StrEnum


class QuantityKind(StrEnum):
    """Measurement kind enum."""

    NONE = "NONE"
    UV_INDEX = "UV_INDEX"
    BRIGHTNESS = "BRIGHTNESS"
    AIR_HUMIDITY = "AIR_HUMIDITY"
    SOIL_HUMIDITY = "SOIL_HUMIDITY"
    RELATIVE_TEMPARATURE = "RELATIVE_TEMPARATURE"
    TEMPERATURE = "TEMPARATURE"
    MOTION = "MOTION"
