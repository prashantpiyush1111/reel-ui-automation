from pathlib import Path


def test_setup_checker_exists():
    path = Path("tools/check_setup.py")
    assert path.is_file()
    assert '"pyperclip"' in path.read_text(encoding="utf-8")
