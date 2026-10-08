from src.config import BotConfig
from src.controller import SafeController
from src.mock_engine import MockEngine
from src.mock_ui import MockUI
from src.workflow import Workflow


def main() -> None:
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)
    comments = (
        "Demo comment 1",
        "Demo comment 2",
        "Demo comment 3",
        "Demo comment 4",
        "Demo comment 5",
        "Demo comment 6",
        "Demo comment 7",
        "Demo comment 8",
    )
    comments_per_reel = 4
    reel_groups = tuple(
        comments[index : index + comments_per_reel]
        for index in range(0, len(comments), comments_per_reel)
    )

    print("Offline automatic Reel workflow demo")
    for reel_number, reel_comments in enumerate(reel_groups, start=1):
        steps = (
            ("reel detection", engine.detect_reel),
            ("open comments", engine.open_comments),
        )

        for label, action in steps:
            if not action():
                raise SystemExit(f"Step failed on reel {reel_number}: {label}")
            print(f"[OK] Reel {reel_number} | {label}: {workflow.state.name}")

        for comment_number, comment in enumerate(reel_comments, start=1):
            if not engine.prepare_comment(comment):
                raise SystemExit(
                    f"Step failed on reel {reel_number}, comment {comment_number}: prepare"
                )
            if not engine.post_comment():
                raise SystemExit(
                    f"Step failed on reel {reel_number}, comment {comment_number}: submit"
                )
            print(
                f"[OK] Reel {reel_number} | comment {comment_number}: "
                f"submitted {comment!r} locally"
            )

        if not engine.close_comments():
            raise SystemExit(f"Step failed on reel {reel_number}: close comments")
        print(f"[OK] Reel {reel_number} | close comments: {workflow.state.name}")

        if reel_number < len(reel_groups):
            if not engine.next_reel():
                raise SystemExit(f"Step failed on reel {reel_number}: next reel")
            print(f"[OK] Reel {reel_number} | next reel: {ui.reel_number}")

    print(f"Submitted locally: {ui.submitted_comments!r}")
    print("Local mock only: automatic submit is not connected to any real platform.")


if __name__ == "__main__":
    main()
