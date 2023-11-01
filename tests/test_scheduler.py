from src.scheduler import Scheduler


def test_scheduler_is_running_getter():
    """Test that the scheduler is not running by default."""

    scheduler: Scheduler = Scheduler(0)

    assert scheduler.running is False


def test_scheduler_start_schedule_method():
    """Test that the scheduler can be started."""

    scheduler: Scheduler = Scheduler(0)

    scheduler.start()
    assert scheduler.running is True


def test_scheduler_stop_schedule_method():
    """Test that the scheduler can be stopped."""

    scheduler: Scheduler = Scheduler(0)

    scheduler.start()
    scheduler.stop()
    assert scheduler.running is False
