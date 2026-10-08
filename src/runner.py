import logging
import time

from .actions import UIActions
from .config import BotConfig
from .controller import SafeController
from .detection_service import DetectionService
from .workflow import State, Workflow


class WorkflowRunner:
    def __init__(self, config: BotConfig):
        self.config = config
        self.controller = SafeController(config)
        self.detector = DetectionService(config)
        self.actions = UIActions(self.controller)
        self.workflow = Workflow()
        self.log = logging.getLogger("reel_automation")

    def run_detection_probe(self, template_name: str) -> bool:
        self.workflow.transition(State.WAITING_FOR_REEL)
        match = self.detector.locate(template_name)
        if match is None:
            self.log.info("Template not detected: %s", template_name)
            return False

        self.log.info(
            "Detected %s at (%d, %d), confidence=%.3f",
            match.name,
            match.x,
            match.y,
            match.confidence,
        )
        self.workflow.transition(State.REEL_VISIBLE)
        return True

    def scroll_and_wait(self) -> None:
        self.controller.scroll_next()
        time.sleep(self.config.loop_delay_seconds)
