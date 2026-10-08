import logging
import time

from .actions import UIActions
from .config import BotConfig
from .controller import SafeController
from .detection_service import DetectionService
from .hotkeys import HotkeyMonitor
from .recovery import RecoveryManager
from .workflow import State, Workflow


class WorkflowEngine:
    """Controlled non-posting UI workflow with recovery and emergency controls."""

    def __init__(self, config: BotConfig):
        self.config = config
        self.controller = SafeController(config)
        self.workflow = Workflow()
        self.detector = DetectionService(config)
        self.actions = UIActions(self.controller)
        self.recovery = RecoveryManager(
            self.workflow,
            self.controller,
        )
        self.hotkeys = HotkeyMonitor(self.controller)
        self.log = logging.getLogger("reel_automation")

    def start_controls(self) -> None:
        self.hotkeys.start()

    def stop_controls(self) -> None:
        self.hotkeys.stop()

    def locate(self, template_name: str):
        return self.recovery.run_with_recovery(
            lambda: self.detector.locate(template_name),
            template_name,
        )

    def detect_reel(self) -> bool:
        match = self.locate("reel_marker.png")
        if match is None:
            return False

        self.workflow.transition(State.REEL_VISIBLE)
        self.log.info(
            "Reel detected at %s with confidence %.3f",
            match.center,
            match.confidence,
        )
        return True

    def open_comment_panel(self) -> bool:
        match = self.locate("comment_button.png")
        if match is None:
            return False

        self.controller.wait_if_paused()
        if self.controller.stopped:
            return False

        self.actions.click_match(match)
        self.workflow.transition(State.COMMENT_OPEN)
        return True

    def prepare_comment(self, text: str) -> bool:
        match = self.locate("comment_input.png")
        if match is None:
            return False

        self.controller.wait_if_paused()
        if self.controller.stopped:
            return False

        self.actions.click_match(match)
        self.actions.type_text(text)
        self.workflow.transition(State.READY_FOR_MANUAL_POST)
        self.log.info("Comment prepared; manual posting checkpoint reached.")
        return True

    def close_comment_panel(self) -> bool:
        match = self.locate("close_comment.png")
        if match is None:
            return False

        self.controller.wait_if_paused()
        if self.controller.stopped:
            return False

        self.actions.click_match(match)
        self.workflow.transition(State.CLOSE_COMMENT)
        return True

    def next_reel(self) -> bool:
        self.controller.wait_if_paused()
        if self.controller.stopped:
            return False

        self.controller.scroll_next()
        time.sleep(self.config.loop_delay_seconds)
        self.workflow.transition(State.NEXT_REEL)
        return True
