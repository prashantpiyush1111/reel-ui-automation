import logging
import time

from .actions import UIActions
from .config import BotConfig
from .controller import SafeController
from .detection_service import DetectionService
from .recovery import RecoveryManager
from .retry import retry
from .workflow import State, Workflow


class WorkflowEngine:
    """Connects screen detection, UI actions, state, and recovery."""

    def __init__(self, config: BotConfig):
        self.config = config
        self.controller = SafeController(config)
        self.workflow = Workflow()
        self.detector = DetectionService(config)
        self.actions = UIActions(self.controller)
        self.recovery = RecoveryManager(self.controller, self.workflow)
        self.log = logging.getLogger("reel_automation")

    def locate(self, template_name: str):
        return retry(
            lambda: self.detector.locate(template_name),
            attempts=3,
            delay_seconds=self.config.retry_delay_seconds,
        )

    def open_comment_panel(self) -> bool:
        match = self.locate("comment_button.png")
        if match is None:
            self.recovery.handle_missing_element("comment_button.png")
            return False

        self.actions.click_match(match)
        self.workflow.transition(State.COMMENT_OPEN)
        return True

    def prepare_comment(self, text: str) -> bool:
        match = self.locate("comment_input.png")
        if match is None:
            self.recovery.handle_missing_element("comment_input.png")
            return False

        self.actions.click_match(match)
        self.actions.type_text(text)
        self.workflow.transition(State.READY_FOR_MANUAL_POST)
        self.log.info("Comment text prepared; manual posting checkpoint reached.")
        return True

    def close_comment_panel(self) -> bool:
        match = self.locate("close_comment.png")
        if match is None:
            self.recovery.handle_missing_element("close_comment.png")
            return False

        self.actions.click_match(match)
        self.workflow.transition(State.CLOSE_COMMENT)
        return True

    def next_reel(self) -> None:
        self.controller.scroll_next()
        time.sleep(self.config.loop_delay_seconds)
        self.workflow.transition(State.NEXT_REEL)
