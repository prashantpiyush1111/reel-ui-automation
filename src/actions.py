from typing import Protocol

from .controller import SafeController
from .detector import Match


class ClipboardBackend(Protocol):
    def copy(self, text: str) -> None:
        ...

    def paste(self) -> str:
        ...


class UIActions:
    def __init__(
        self,
        controller: SafeController,
        clipboard_backend: ClipboardBackend | None = None,
        pyautogui_backend=None,
    ):
        self.controller = controller
        self._clipboard = clipboard_backend
        self._pyautogui = pyautogui_backend

    def _get_pyautogui(self):
        if self._pyautogui is None:
            import pyautogui

            self._pyautogui = pyautogui
        return self._pyautogui

    def _get_clipboard(self) -> ClipboardBackend:
        if self._clipboard is None:
            import pyperclip

            self._clipboard = pyperclip
        return self._clipboard

    def click_match(self, match: Match) -> None:
        self.controller.wait_if_paused()
        if self.controller.stopped:
            return

        self._get_pyautogui().click(*match.center)

    def type_text(self, text: str) -> None:
        self.controller.wait_if_paused()
        if self.controller.stopped:
            return

        pyautogui = self._get_pyautogui()
        if text.isascii():
            pyautogui.write(text, interval=0.01)
            return

        clipboard = self._get_clipboard()
        previous_clipboard: str | None = None
        can_restore = False

        try:
            try:
                previous_clipboard = clipboard.paste()
                can_restore = True
            except Exception:
                pass

            clipboard.copy(text)
            self.controller.wait_if_paused()
            if self.controller.stopped:
                return
            pyautogui.hotkey("ctrl", "v")
        finally:
            if can_restore:
                try:
                    clipboard.copy(previous_clipboard or "")
                except Exception:
                    pass
