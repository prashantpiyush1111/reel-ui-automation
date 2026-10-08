import logging
import time

from .config import BotConfig
from .workflow_engine import WorkflowEngine


class StepRunner:
    """Runs the safe, non-posting UI workflow one controlled step at a time."""

    def __init__(self, config: BotConfig):
        self.engine = WorkflowEngine(config)
        self.log = logging.getLogger("reel_automation")

    def start(self) -> None:
        self.engine.start_controls()

    def stop(self) -> None:
        self.engine.stop_controls()

    def detect_reel(self) -> bool:
        return self.engine.detect_reel()

    def open_comments(self) -> bool:
        return self.engine.open_comment_panel()

    def prepare_comment(self, text: str) -> bool:
        return self.engine.prepare_comment(text)

    def close_comments(self) -> bool:
        return self.engine.close_comment_panel()

    def next_reel(self) -> bool:
        return self.engine.next_reel()

    def run_cycle(self, comment: str | None = None) -> bool:
        """Run one safe cycle and stop at the manual-post checkpoint."""
        if not self.detect_reel():
            return False

        if not self.open_comments():
            return False

        if comment is not None and not self.prepare_comment(comment):
            return False

        # No submit/post action is performed here.
        if comment is not None:
            return True

        if not self.close_comments():
            return False

        return self.next_reel()

    def run_cycles(self, comments: tuple[str, ...], cycles: int = 1) -> None:
        """Run bounded safe cycles; never submits comments."""
        self.start()
        try:
            for index in range(max(0, cycles)):
                if self.engine.controller.stopped:
                    break

                comment = comments[index % len(comments)] if comments else None
                if not self.run_cycle(comment):
                    self.log.warning("Cycle %d stopped before completion.", index + 1)
                    break

                if comment is not None:
                    self.log.info(
                        "Manual-post checkpoint reached for cycle %d; stopping run.",
                        index + 1,
                    )
                    break

                time.sleep(self.engine.config.loop_delay_seconds)
        finally:
            self.stop()
