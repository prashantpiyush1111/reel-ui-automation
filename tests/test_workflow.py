from src.config import BotConfig
from src.workflow import State, Workflow


def test_workflow_starts_waiting():
    workflow = Workflow()
    assert workflow.state is State.WAITING_FOR_REEL


def test_workflow_transitions():
    workflow = Workflow()
    workflow.transition(State.COMMENT_OPEN)
    assert workflow.state is State.COMMENT_OPEN
    workflow.reset()
    assert workflow.state is State.WAITING_FOR_REEL
