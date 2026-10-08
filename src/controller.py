import time

import pyautogui

from .config import BotConfig


class SafeController:
    def __init__(self, config: BotConfig):
        self.config = config
        self.paused = False
        self.stopped = False

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    def stop(self) -> None:
        self.stopped = True

    def wait_if_paused(self) -> None:
        while self.paused and not self.stopped:
            time.sleep(0.2)

    def scroll_next(self) -> None:
        self.wait_if_paused()
        if self.stopped:
            return
        pyautogui.scroll(self.config.scroll_amount)
