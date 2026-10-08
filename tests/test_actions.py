from src.actions import UIActions
from src.config import BotConfig
from src.controller import SafeController


class FakeClipboard:
    def __init__(self, value: str = "old clipboard"):
        self.value = value
        self.copied: list[str] = []

    def copy(self, text: str) -> None:
        self.copied.append(text)
        self.value = text

    def paste(self) -> str:
        return self.value


class FakePyAutoGUI:
    def __init__(self):
        self.writes = []
        self.hotkeys = []

    def write(self, text: str, interval: float) -> None:
        self.writes.append((text, interval))

    def hotkey(self, *keys: str) -> None:
        self.hotkeys.append(keys)


def test_ascii_typing_uses_write():
    keyboard = FakePyAutoGUI()
    actions = UIActions(SafeController(BotConfig()), pyautogui_backend=keyboard)

    actions.type_text("Hello 123")

    assert keyboard.writes == [("Hello 123", 0.01)]
    assert keyboard.hotkeys == []


def test_unicode_typing_uses_clipboard_and_restores_previous_value():
    clipboard = FakeClipboard("keep me")
    keyboard = FakePyAutoGUI()
    actions = UIActions(
        SafeController(BotConfig()),
        clipboard_backend=clipboard,
        pyautogui_backend=keyboard,
    )

    actions.type_text("नमस्ते 👋")

    assert clipboard.copied == ["नमस्ते 👋", "keep me"]
    assert clipboard.value == "keep me"
    assert keyboard.hotkeys == [("ctrl", "v")]
    assert keyboard.writes == []


def test_unicode_typing_still_works_when_clipboard_cannot_be_read():
    class WriteOnlyClipboard:
        def __init__(self):
            self.copied = []

        def copy(self, text: str) -> None:
            self.copied.append(text)

        def paste(self) -> str:
            raise RuntimeError("clipboard unavailable")

    clipboard = WriteOnlyClipboard()
    keyboard = FakePyAutoGUI()
    actions = UIActions(
        SafeController(BotConfig()),
        clipboard_backend=clipboard,
        pyautogui_backend=keyboard,
    )

    actions.type_text("हिंदी ❤️")

    assert clipboard.copied == ["हिंदी ❤️"]
    assert keyboard.hotkeys == [("ctrl", "v")]
