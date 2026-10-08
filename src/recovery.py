import logging

from .controller import SafeController
from .workflow import State, Workflow


class RecoveryManager:
    def __init__(self, controller: SafeController, workflow: Workflow):
        self.controller = controller
        self.workflow = workflow
        self.log = logging.getLogger("reel_automation")

    def handle_missing_element(self, element_name: str) -> None:
        self.log.warning("UI element not found: %s", element_name)
        self.workflow.transition(State.WAITING_FOR_REEL)

    def fail_safe(self, reason: str) -> None:
        self.log.error("Fail-safe stop: %s", reason)
        self.workflow.transition(State.STOPPED)
        self.controller.stop()
