from src.controller import SafeController
from src.recovery import RecoveryManager, RecoveryPolicy
from src.workflow import State, Workflow


def test_recovery_retries_then_succeeds():
    workflow = Workflow()
    controller = SafeController()
    manager = RecoveryManager(
        workflow,
        controller,
        RecoveryPolicy(attempts=3, initial_delay_seconds=0, backoff=1),
    )

    calls = {"count": 0}

    def operation():
        calls["count"] += 1
        return "ok" if calls["count"] == 2 else None

    assert manager.run_with_recovery(operation, "test") == "ok"
    assert calls["count"] == 2
    assert workflow.state == State.WAITING_FOR_REEL


def test_recovery_handles_exceptions():
    workflow = Workflow()
    controller = SafeController()
    manager = RecoveryManager(
        workflow,
        controller,
        RecoveryPolicy(attempts=2, initial_delay_seconds=0),
    )

    calls = {"count": 0}

    def operation():
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("temporary failure")
        return "ok"

    assert manager.run_with_recovery(operation, "test") == "ok"
    assert calls["count"] == 2


def test_recovery_returns_none_after_exhaustion():
    workflow = Workflow()
    controller = SafeController()
    manager = RecoveryManager(
        workflow,
        controller,
        RecoveryPolicy(attempts=2, initial_delay_seconds=0),
    )

    assert manager.run_with_recovery(lambda: None, "test") is None
    assert workflow.state == State.WAITING_FOR_REEL
    assert not controller.stopped


def test_fail_safe_stops_controller():
    workflow = Workflow()
    controller = SafeController()
    manager = RecoveryManager(workflow, controller)

    manager.fail_safe("test failure")

    assert workflow.state == State.STOPPED
    assert controller.stopped
