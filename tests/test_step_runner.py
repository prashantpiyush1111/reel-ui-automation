from src.config import BotConfig
from src.step_runner import StepRunner
from src.workflow import State


def test_step_runner_starts_with_safe_controls():
    runner = StepRunner(BotConfig())

    assert runner.engine.workflow.state == State.WAITING_FOR_REEL
    assert not runner.engine.controller.stopped
    assert not runner.engine.controller.paused
