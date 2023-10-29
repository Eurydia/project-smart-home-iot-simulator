"""Module for logger."""

from dataclasses import dataclass
from typing import Callable, TextIO


@dataclass
class SchedulerLogger:
    """Logger that can be used to log messages."""

    log_file: TextIO
    log_function: Callable[[str], None]

    def add_log(self, log: str) -> None:
        """Log a message to a file and a stream."""

        self.log_function(log)

        with open(
            self.log_file.name,
            mode="a",
            encoding="utf-8",
        ) as file:
            file.write(log + "\n")
