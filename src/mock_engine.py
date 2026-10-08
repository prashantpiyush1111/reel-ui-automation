from dataclasses import dataclass

from .controller import SafeController
from .mock_ui import MockUI
from .workflow import State, Workflow


@dataclass
class MockEngine:
    """Offline equivalent of the safe workflow engine for integration tests."""

    ui: MockUI
    controller: SafeController
    workflow: Workflow

    def locate(self, template_name: str):
        if self.controller.stopped:
            return None
        self.controller.wait_if_paused()
        return self.ui.locate(template_name)

    def click(self, match) -> None:
        if self.controller.stopped:
            return
        self.controller.wait_if_paused()
        self.ui.click(match)

    def type_text(self, text: str) -> None:
        if self.controller.stopped:
            return
        self.controller.wait_if_paused()
        self.ui.type_text(text)

    def detect_reel(self) -> bool:
        match = self.locate("reel_marker.png")
        if match is None:
            return False
        self.workflow.transition(State.REEL_VISIBLE)
        return True

    def open_comments(self) -> bool:
        match = self.locate("comment_button.png")
        if match is None:
            return False
        self.click(match)
        self.workflow.transition(State.COMMENT_OPEN)
        return True

    def prepare_comment(self, text: str) -> bool:
        match = self.locate("comment_input.png")
        if match is None:
            return False
        self.click(match)
        self.type_text(text)
        self.workflow.transition(State.READY_FOR_MANUAL_POST)
        return True

    def close_comments(self) -> bool:
        match = self.locate("close_comment.png")
        if match is None:
            return False
        self.click(match)
        self.workflow.transition(State.CLOSE_COMMENT)
        return True

    def next_reel(self) -> bool:
        if self.controller.stopped:
            return False
        self.controller.wait_if_paused()
        self.ui.scroll()
        self.workflow.transition(State.NEXT_REEL)
        return True
