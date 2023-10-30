from tempfile import NamedTemporaryFile

from src.schedulers.scheduler import Scheduler
from src.schedulers.scheduler_logger import SchedulerLogger


def test_scheduler_is_running_getter():
    """Test that the scheduler is not running by default."""

    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
    ) as temp_file:
        test_logger = SchedulerLogger(
            temp_file,
            lambda _: None,
        )

        scheduler: Scheduler = Scheduler(
            test_logger,
            0,
        )

        assert scheduler.is_running() is False


def test_scheduler_start_schedule_method():
    """Test that the scheduler can be started."""

    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
    ) as temp_file:
        test_logger = SchedulerLogger(
            temp_file,
            lambda _: None,
        )

        scheduler: Scheduler = Scheduler(
            test_logger,
            0,
        )

        scheduler.start_schedule(debug=True)

        assert scheduler.is_running() is True


def test_scheduler_start_schedule_method_prevent_multiple_starts():
    """Test that the scheduler can be started only once."""

    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
    ) as temp_file:
        test_logger = SchedulerLogger(
            temp_file,
            lambda _: None,
        )

        scheduler: Scheduler = Scheduler(
            test_logger,
            0,
        )

        scheduler.start_schedule(debug=True)
        scheduler.start_schedule(debug=True)

        assert scheduler.is_running() is False


def test_scheduler_stop_schedule_method():
    """Test that the scheduler can be stopped."""

    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
    ) as temp_file:
        test_logger = SchedulerLogger(
            temp_file,
            lambda _: None,
        )

        scheduler: Scheduler = Scheduler(
            test_logger,
            0,
        )

        scheduler.start_schedule(debug=True)
        scheduler.stop_schedule()

        assert scheduler.is_running() is False
