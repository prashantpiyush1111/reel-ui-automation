import threading
import time

from .controller import SafeController


class HotkeyMonitor:
    """Global keyboard monitor for local pause/resume/stop controls."""

    PAUSE_KEY = "f8"
    STOP_KEY = "f9"

    def __init__(self, controller: SafeController, keyboard_module=None):
        self.controller = controller
        self.keyboard = keyboard_module
        self._thread = None
        self._running = False

    def start(self) -> None:
        if self._running:
            return

        if self.keyboard is None:
            try:
                import keyboard as keyboard_module
            except ImportError:
                return
            self.keyboard = keyboard_module

        self._running = True
        self.keyboard.on_press_key(self.PAUSE_KEY, self._toggle_pause)
        self.keyboard.on_press_key(self.STOP_KEY, self._stop)
        self._thread = threading.Thread(target=self._keep_alive, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

        if self.keyboard is not None:
            try:
                self.keyboard.unhook_all()
            except Exception:
                pass

    def _toggle_pause(self, _event=None) -> None:
        if self.controller.paused:
            self.controller.resume()
        else:
            self.controller.pause()

    def _stop(self, _event=None) -> None:
        self.controller.stop()

    def _keep_alive(self) -> None:
        while self._running and not self.controller.stopped:
            time.sleep(0.1)
