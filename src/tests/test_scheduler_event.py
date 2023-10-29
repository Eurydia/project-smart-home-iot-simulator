from src.schedulers.scheduler_event import SchedulerEvent


def test_scheduler_event_should_trigger_method_empty():
    """Test that the scheduler event should trigger."""

    scheduler_event: SchedulerEvent = SchedulerEvent(
        requirements=[],
        actions=[],
    )
    assert scheduler_event.should_trigger() is True


def test_scheduler_event_should_trigger_method():
    """Test that the scheduler event should trigger."""

    scheduler_event: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: True,
        ],
        actions=[],
    )
    assert scheduler_event.should_trigger() is True


def test_scheduler_event_should_trigger_method_no():
    """Test that the scheduler event should not trigger."""

    scheduler_event: SchedulerEvent = SchedulerEvent(
        requirements=[
            lambda: False,
        ],
        actions=[],
    )
    assert scheduler_event.should_trigger() is False


def test_scheduler_event_trigger_action_method():
    """Test that actions can be triggered."""

    scheduler_event: SchedulerEvent = SchedulerEvent(
        requirements=[],
        actions=[
            lambda: "action",
        ],
    )

    assert scheduler_event.trigger_actions() == ["action"]
