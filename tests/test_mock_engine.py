from src.config import BotConfig
from src.controller import SafeController
from src.mock_engine import MockEngine
from src.mock_ui import MockUI
from src.workflow import State, Workflow


def test_mock_engine_safe_comment_flow():
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)

    assert engine.detect_reel()
    assert workflow.state == State.REEL_VISIBLE

    assert engine.open_comments()
    assert workflow.state == State.COMMENT_OPEN

    assert engine.prepare_comment("demo comment")
    assert ui.typed_text == "demo comment"
    assert workflow.state == State.READY_FOR_MANUAL_POST

    # The mock engine deliberately has no post/submit method.
    assert not hasattr(engine, "post_comment")

    assert engine.close_comments()
    assert workflow.state == State.CLOSE_COMMENT

    assert engine.next_reel()
    assert workflow.state == State.NEXT_REEL
