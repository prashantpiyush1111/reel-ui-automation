from pathlib import Path


def test_setup_checker_exists():
    assert Path("tools/check_setup.py").is_file()
