from enum import Enum, auto


class State(Enum):
    WAITING_FOR_REEL = auto()
    REEL_VISIBLE = auto()
    COMMENT_OPEN = auto()
    READY_FOR_MANUAL_POST = auto()
    CLOSE_COMMENT = auto()
    NEXT_REEL = auto()
    STOPPED = auto()


class Workflow:
    """Explicit state machine for the safe UI workflow."""

    def __init__(self) -> None:
        self.state = State.WAITING_FOR_REEL

    def transition(self, state: State) -> None:
        self.state = state

    def reset(self) -> None:
        self.state = State.WAITING_FOR_REEL
