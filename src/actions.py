from .controller import SafeController
from .detector import Match


class UIActions:
    def __init__(self, controller: SafeController):
        self.controller = controller

    def click_match(self, match: Match) -> None:
        self.controller.wait_if_paused()
        if self.controller.stopped:
            return
        import pyautogui

        pyautogui.click(*match.center)

    def type_text(self, text: str) -> None:
        self.controller.wait_if_paused()
        if self.controller.stopped:
            return
        import pyautogui

        pyautogui.write(text, interval=0.01)
