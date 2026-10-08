from pathlib import Path

import cv2
import numpy as np

from src.template_validator import inspect_template, validate_templates


def test_inspect_template(tmp_path: Path):
    path = tmp_path / "sample.png"
    image = np.zeros((24, 40, 3), dtype=np.uint8)
    cv2.imwrite(str(path), image)

    info = inspect_template(path)

    assert info.width == 40
    assert info.height == 24
    assert info.channels == 3


def test_validate_templates_reports_missing(tmp_path: Path):
    errors = validate_templates(tmp_path, ("missing.png",))

    assert errors == ["Missing template: missing.png"]


def test_validate_templates_accepts_readable_template(tmp_path: Path):
    path = tmp_path / "reel_marker.png"
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    cv2.imwrite(str(path), image)

    errors = validate_templates(tmp_path, ("reel_marker.png",))

    assert errors == []
