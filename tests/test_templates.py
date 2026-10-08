from pathlib import Path

from src.templates import REQUIRED_TEMPLATES, validate_template_dir


def test_required_template_names_are_unique():
    assert len(REQUIRED_TEMPLATES) == len(set(REQUIRED_TEMPLATES))


def test_missing_templates_are_reported(tmp_path: Path):
    missing = validate_template_dir(tmp_path)
    assert set(missing) == set(REQUIRED_TEMPLATES)
