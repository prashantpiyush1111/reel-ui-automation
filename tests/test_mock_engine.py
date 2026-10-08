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

    assert engine.close_comments()
    assert workflow.state == State.CLOSE_COMMENT

    assert engine.next_reel()
    assert workflow.state == State.NEXT_REEL


def test_mock_engine_can_auto_submit_locally():
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)

    assert engine.detect_reel()
    assert engine.open_comments()
    assert engine.prepare_comment("local comment")
    assert engine.post_comment()

    assert ui.submitted_comments == ["local comment"]
    assert ui.typed_text == ""

    assert engine.close_comments()
    assert engine.next_reel()


def test_mock_engine_runs_four_comments_on_one_reel():
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)

    comments = ("one", "two", "three", "four")
    assert engine.detect_reel()
    assert engine.open_comments()

    for comment in comments:
        assert engine.prepare_comment(comment)
        assert engine.post_comment()

    assert engine.close_comments()
    assert ui.submitted_comments == list(comments)
    assert ui.reel_number == 1


def test_mock_engine_runs_two_reels_with_four_comments_each():
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)

    comments = tuple(f"comment {index}" for index in range(1, 9))
    for reel_index in range(2):
        assert engine.detect_reel()
        assert engine.open_comments()

        for comment in comments[reel_index * 4 : (reel_index + 1) * 4]:
            assert engine.prepare_comment(comment)
            assert engine.post_comment()

        assert engine.close_comments()
        if reel_index == 0:
            assert engine.next_reel()

    assert ui.submitted_comments == list(comments)
    assert ui.reel_number == 2
