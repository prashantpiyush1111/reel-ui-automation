import logging
import time

from .config import BotConfig
from .workflow_engine import WorkflowEngine
from .workflow import State


class StepRunner:
    """Runs the non-posting UI workflow one controlled step at a time."""

    def __init__(self, config: BotConfig):
        self.engine = WorkflowEngine(config)
        self.log = logging.getLogger("reel_automation")

    def detect_reel(self) -> bool:
        match = self.engine.locate("reel_marker.png")
        if match is None:
            self.engine.recovery.handle_missing_element("reel_marker.png")
            return False
        self.engine.workflow.transition(State.REEL_VISIBLE)
        return True

    def open_comments(self) -> bool:
        return self.engine.open_comment_panel()

    def prepare_comment(self, text: str) -> bool:
        return self.engine.prepare_comment(text)

    def close_comments(self) -> bool:
        return self.engine.close_comment_panel()

    def next_reel(self) -> None:
        self.engine.next_reel()
        time.sleep(self.engine.config.loop_delay_seconds)
