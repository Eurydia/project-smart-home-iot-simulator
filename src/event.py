from dataclasses import dataclass
from typing import Callable, TypeAlias


@dataclass
class Event:
    """Represents an event that can be triggered when certain conditions are met.

    Usage:
    Example:

        ```python
        def check_if_user_is_logged_in() -> bool:
            return current_user is not None

        def send_welcome_email() -> None:
            print("Sending welcome email...")

        event = Event(
            name="user_logged_in",
            act=send_welcome_email,
            requirements=[check_if_user_is_logged_in],
        )

        # Add the event to a scheduler.
        scheduler.add_event(event)

        # The scheduler will periodically run the should_trigger() method of the event.
        # If the method returns True, the scheduler will call the act() method of the event.
        ```
    """

    name: str
    act: Callable[[], str]
    requirements: list[Callable[[], bool]]

    def should_trigger(self) -> bool:
        """Returns True if the event should be triggered, False otherwise."""
        return all(req() for req in self.requirements)

    def trigger(self) -> str:
        return self.act()
