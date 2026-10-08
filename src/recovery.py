import logging
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

from .controller import SafeController
from .workflow import State, Workflow

T = TypeVar("T")


@dataclass(frozen=True)
class RecoveryPolicy:
    attempts: int = 3
    initial_delay_seconds: float = 0.35
    backoff: float = 2.0
    max_delay_seconds: float = 2.0


class RecoveryManager:
    def __init__(
        self,
        workflow: Workflow,
        controller: SafeController,
        policy: RecoveryPolicy | None = None,
        logger: logging.Logger | None = None,
    ):
        self.workflow = workflow
        self.controller = controller
        self.policy = policy or RecoveryPolicy()
        self.logger = logger or logging.getLogger(__name__)

    def run_with_recovery(
        self,
        operation: Callable[[], T | None],
        description: str,
    ) -> T | None:
        delay = max(0.0, self.policy.initial_delay_seconds)
        attempts = max(1, self.policy.attempts)

        for attempt in range(1, attempts + 1):
            if self.controller.stopped:
                self.logger.info("Recovery cancelled because controller is stopped")
                return None

            try:
                result = operation()
            except Exception as exc:
                self.logger.warning(
                    "%s failed on attempt %d/%d: %s",
                    description,
                    attempt,
                    attempts,
                    exc,
                )
                result = None

            if result is not None:
                if attempt > 1:
                    self.logger.info("%s recovered on attempt %d", description, attempt)
                return result

            if attempt < attempts:
                self.logger.info(
                    "%s not ready; retrying in %.2fs",
                    description,
                    delay,
                )
                if delay > 0:
                    time.sleep(delay)
                delay = min(
                    self.policy.max_delay_seconds,
                    delay * max(1.0, self.policy.backoff),
                )

        self.handle_missing_element(description)
        return None

    def handle_missing_element(self, description: str = "UI element"):
        self.logger.warning(
            "Unable to recover %s; returning to safe waiting state",
            description,
        )
        self.workflow.transition(State.WAITING_FOR_REEL)

    def fail_safe(self, reason: str = "unrecoverable workflow error"):
        self.logger.error("Fail-safe stop: %s", reason)
        self.workflow.transition(State.STOPPED)
        self.controller.stop()
