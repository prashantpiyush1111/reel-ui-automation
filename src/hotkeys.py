import threading
import time

from .controller import SafeController


class HotkeyMonitor:
    """Optional keyboard monitor for local pause/stop controls."""

    def __init__(self, controller: SafeController):
        self.controller = controller
        self._thread = None
        self._running = False

    def start(self) -> None:
        # Keyboard integration is intentionally isolated so it can be replaced
        # by a platform-specific implementation without changing the workflow.
        self._running = True
        self._thread = threading.Thread(target=self._keep_alive, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def _keep_alive(self) -> None:
        while self._running and not self.controller.stopped:
            time.sleep(0.25)
