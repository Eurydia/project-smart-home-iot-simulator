"""Module for logger."""

from typing import Callable, TextIO


class Logger:
    """Logger that can be used to log messages."""

    def __init__(
        self,
        log_file: TextIO,
        log_function: Callable[[str], None],
    ) -> None:
        self._log_file = log_file
        self._log_function = log_function

    def log_text(self, loggable_text: str) -> None:
        """Log a message to a file and a stream.

        Parameters
        ----------
        loinable_text : str
            The message to log.
        """

        self._log_function(loggable_text)

        with open(
            self._log_file.name,
            mode="a",
            encoding="utf-8",
        ) as file:
            file.write(loggable_text + "\n")

    def log_texts(self, loggable_texts: list[str]) -> None:
        """Log a message to a file and a stream.

        Parameters
        ----------
        loinable_texts : list[str]
            A list of messages to log.
        """

        for loggable_text in loggable_texts:
            self.log_text(loggable_text)
