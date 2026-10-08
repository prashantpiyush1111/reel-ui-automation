from src.config import BotConfig
from src.controller import SafeController
from src.mock_engine import MockEngine
from src.mock_ui import MockUI
from src.workflow import State, Workflow


def main() -> None:
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)

    steps = [
        ("reel detection", engine.detect_reel),
        ("open comments", engine.open_comments),
        ("prepare comment", lambda: engine.prepare_comment("Demo comment")),
        ("close comments", engine.close_comments),
        ("next reel", engine.next_reel),
    ]

    print("Offline workflow integration demo")
    for label, action in steps:
        if not action():
            raise SystemExit(f"Step failed: {label}")
        print(f"[OK] {label}: {workflow.state.name}")

    print(f"Typed text: {ui.typed_text!r}")
    print("Manual-post checkpoint was respected: no submit action exists.")


if __name__ == "__main__":
    main()
