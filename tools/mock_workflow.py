from src.config import BotConfig
from src.controller import SafeController
from src.mock_engine import MockEngine
from src.mock_ui import MockUI
from src.workflow import State, Workflow


def main() -> None:
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)
    comments = (
        "Demo comment 1",
        "Demo comment 2",
        "Demo comment 3",
        "Demo comment 4",
    )

    print("Offline automatic Reel workflow demo")
    for reel_number, comment in enumerate(comments, start=1):
        steps = (
            ("reel detection", engine.detect_reel),
            ("open comments", engine.open_comments),
            ("prepare comment", lambda text=comment: engine.prepare_comment(text)),
            ("auto submit (local mock)", engine.post_comment),
            ("close comments", engine.close_comments),
        )

        for label, action in steps:
            if not action():
                raise SystemExit(f"Step failed on reel {reel_number}: {label}")
            print(f"[OK] Reel {reel_number} | {label}: {workflow.state.name}")

        if reel_number < len(comments):
            if not engine.next_reel():
                raise SystemExit(f"Step failed on reel {reel_number}: next reel")
            print(f"[OK] Reel {reel_number} | next reel: {ui.reel_number}")

    print(f"Submitted locally: {ui.submitted_comments!r}")
    print("Local mock only: automatic submit is not connected to any real platform.")


if __name__ == "__main__":
    main()
