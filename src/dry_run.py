import logging

from .config import BotConfig
from .workflow import State, Workflow


class DryRun:
    """Simulates workflow transitions without interacting with a live platform."""

    def __init__(self, config: BotConfig):
        self.config = config
        self.workflow = Workflow()
        self.log = logging.getLogger("reel_automation")

    def execute(self) -> list[str]:
        states = [
            State.WAITING_FOR_REEL,
            State.REEL_VISIBLE,
            State.COMMENT_OPEN,
            State.READY_FOR_MANUAL_POST,
            State.CLOSE_COMMENT,
            State.NEXT_REEL,
        ]
        visited = []
        for state in states:
            self.workflow.transition(state)
            visited.append(state.name)
            self.log.info("DRY-RUN state: %s", state.name)
        return visited
