import argparse

from .config import BotConfig
from .controller import SafeController
from .dry_run import DryRun
from .logger import configure_logging
from .mock_engine import MockEngine
from .mock_ui import MockUI
from .settings import load_config
from .workflow import Workflow
from .workflow_engine import WorkflowEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safe Reel UI workflow runner (manual-post checkpoint)."
    )
    parser.add_argument("--live", action="store_true", help="Enable live screen/UI interaction.")
    parser.add_argument("--mock", action="store_true", help="Run the complete workflow against the offline mock UI.")
    parser.add_argument("--config", default=None, help="Optional JSON config file.")
    parser.add_argument(
        "--comment",
        action="append",
        default=[],
        help="Comment text to prepare. Repeat the flag for multiple predefined comments.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one live workflow cycle instead of looping.",
    )
    return parser


def run_cycle(engine: WorkflowEngine, comments: tuple[str, ...]) -> bool:
    if not engine.detect_reel():
        engine.log.warning("Active Reel UI was not detected.")
        return False

    if not engine.open_comment_panel():
        engine.log.warning("Comment panel could not be opened.")
        return False

    for text in comments:
        if not engine.prepare_comment(text):
            engine.log.warning("Comment input could not be prepared.")
            return False
        print(
            f"Prepared comment: {text!r}. "
            "Manual-post checkpoint reached; submit it yourself if desired."
        )
        input("Press Enter after the manual-post decision to continue... ")

    if not engine.close_comment_panel():
        engine.log.warning("Comment panel could not be closed.")
        return False

    return engine.next_reel()


def run_mock(comment: str = "Demo comment") -> None:
    ui = MockUI()
    workflow = Workflow()
    engine = MockEngine(ui, SafeController(BotConfig()), workflow)

    if not engine.detect_reel():
        raise RuntimeError("Mock step failed: reel detection")
    print(f"[OK] reel detection: {workflow.state.name}")

    if not engine.open_comments():
        raise RuntimeError("Mock step failed: open comments")
    print(f"[OK] open comments: {workflow.state.name}")

    if not engine.prepare_comment(comment):
        raise RuntimeError("Mock step failed: prepare comment")
    print(f"[OK] prepare comment: {workflow.state.name}")
    print(f"Prepared text: {ui.typed_text!r}")
    print("Manual-post checkpoint reached; no submit action exists.")

    if not engine.close_comments():
        raise RuntimeError("Mock step failed: close comments")
    print(f"[OK] close comments: {workflow.state.name}")

    if not engine.next_reel():
        raise RuntimeError("Mock step failed: next reel")
    print(f"[OK] next reel: {workflow.state.name}")


def run(
    config: BotConfig | None = None,
    comments: tuple[str, ...] = (),
    live: bool = False,
    once: bool = False,
    mock: bool = False,
) -> None:
    configure_logging()

    if mock:
        run_mock(comments[0] if comments else "Demo comment")
        return

    if not live:
        visited = DryRun(config or BotConfig()).execute()
        print("Safe dry run complete.")
        print(" -> ".join(visited))
        return

    if not comments:
        raise ValueError("Live mode requires at least one --comment value.")

    engine = WorkflowEngine(config or BotConfig())
    engine.start_controls()

    try:
        while not engine.controller.stopped:
            if not run_cycle(engine, comments):
                if once:
                    break
                engine.workflow.reset()
                continue

            if once:
                break

            engine.workflow.reset()
    except KeyboardInterrupt:
        engine.controller.stop()
        print("Stopped safely.")
    finally:
        engine.stop_controls()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.live and args.mock:
        parser.error("--live and --mock cannot be used together.")

    config = load_config(args.config)
    comments = tuple(args.comment)

    run(
        config=config,
        comments=comments,
        live=args.live,
        once=args.once,
        mock=args.mock,
    )


if __name__ == "__main__":
    main()
