import threading
import time

from .config import BotConfig


class SafeController:
    def __init__(self, config: BotConfig):
        self.config = config
        self._lock = threading.RLock()
        self._paused = False
        self._stopped = False

    @property
    def paused(self) -> bool:
        with self._lock:
            return self._paused

    @property
    def stopped(self) -> bool:
        with self._lock:
            return self._stopped

    def pause(self) -> None:
        with self._lock:
            if not self._stopped:
                self._paused = True

    def resume(self) -> None:
        with self._lock:
            if not self._stopped:
                self._paused = False

    def stop(self) -> None:
        with self._lock:
            self._stopped = True
            self._paused = False

    def wait_if_paused(self) -> None:
        while self.paused and not self.stopped:
            time.sleep(0.1)

    def scroll_next(self) -> None:
        self.wait_if_paused()
        if self.stopped:
            return
        import pyautogui

        pyautogui.scroll(self.config.scroll_amount)
