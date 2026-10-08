from types import SimpleNamespace

import src.diagnostics as diagnostics


def test_print_screen_info_reports_matching_sizes(monkeypatch, capsys):
    monkeypatch.setattr(
        diagnostics,
        "capture_screen",
        lambda: SimpleNamespace(width=1920, height=1080),
    )

    class FakePyAutoGUI:
        @staticmethod
        def size():
            return (1920, 1080)

    monkeypatch.setitem(__import__("sys").modules, "pyautogui", FakePyAutoGUI)

    diagnostics.print_screen_info()

    output = capsys.readouterr().out
    assert "Screenshot: 1920x1080" in output
    assert "PyAutoGUI:  1920x1080" in output
    assert "Coordinate sizes match." in output


def test_print_screen_info_warns_on_mismatch(monkeypatch, capsys):
    monkeypatch.setattr(
        diagnostics,
        "capture_screen",
        lambda: SimpleNamespace(width=1920, height=1080),
    )

    class FakePyAutoGUI:
        @staticmethod
        def size():
            return (1536, 864)

    monkeypatch.setitem(__import__("sys").modules, "pyautogui", FakePyAutoGUI)

    diagnostics.print_screen_info()

    output = capsys.readouterr().out
    assert "WARNING: screenshot and PyAutoGUI coordinate sizes do not match." in output
