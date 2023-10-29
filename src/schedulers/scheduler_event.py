"""Module for scheduler event."""


from dataclasses import dataclass
from typing import Callable


@dataclass
class SchedulerEvent:
    """Scheduler event that can be triggered by a set of requirements and actions."""

    actions: list[Callable[[], str]]
    requirements: list[Callable[[], bool]]

    def should_trigger(self) -> bool:
        """Check if all requirements are met."""
        return all(req() for req in self.requirements)

    def trigger_actions(self) -> list[str]:
        """Trigger all actions and return the log."""
        return [action() for action in self.actions]
