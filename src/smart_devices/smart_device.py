from dataclasses import dataclass, field


@dataclass
class SmartDevice:
    name: str
    uuid: int

    running: bool = field(init=False, default=False)
