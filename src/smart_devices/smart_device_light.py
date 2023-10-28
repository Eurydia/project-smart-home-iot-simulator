from dataclasses import dataclass, field


from src.smart_devices.smart_device import SmartDevice


@dataclass
class SmartDeviceLight(SmartDevice):
    brightness_level_min: int = field(default=0)
    brightness_level_max: int = field(default=100)

    _brightness_level: int = field(init=False)

    def __post_init__(self) -> None:
        self._brightness_level: int = self.brightness_level_min

    def turn_off(self) -> str:
        self._brightness_level = 0
        self.running = False
        return f"{self.name}: Turning off."

    def set_brightness_level(self, new_brightness_level: int) -> str:
        if new_brightness_level > self.brightness_level_max:
            return

        if new_brightness_level < self.brightness_level_min:
            return
        self.running = True
        self._brightness_level = new_brightness_level
        return f"{self.name}: Setting brightness level to {new_brightness_level}."
