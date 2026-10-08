from pathlib import Path

import cv2
import numpy as np

from src.detector import TemplateDetector
from src.screen import ScreenFrame


def test_detector_finds_template(tmp_path: Path):
    template = np.zeros((20, 30, 3), dtype=np.uint8)
    template[5:15, 8:22] = 255

    source = np.zeros((100, 120, 3), dtype=np.uint8)
    source[40:60, 50:80] = template

    template_path = tmp_path / "marker.png"
    cv2.imwrite(str(template_path), template)

    frame = ScreenFrame(source, 120, 100)
    detector = TemplateDetector(tmp_path, confidence=0.9)

    match = detector.find(frame, "marker.png")

    assert match is not None
    assert match.x == 50
    assert match.y == 40
    assert match.width == 30
    assert match.height == 20
    assert match.scale == 1.0
    assert match.confidence >= 0.9


def test_detector_supports_custom_scales(tmp_path: Path):
    template = np.zeros((10, 10, 3), dtype=np.uint8)
    template[2:8, 2:8] = 255

    scaled = cv2.resize(template, (15, 15), interpolation=cv2.INTER_CUBIC)
    source = np.zeros((60, 60, 3), dtype=np.uint8)
    source[20:35, 25:40] = scaled

    template_path = tmp_path / "scaled.png"
    cv2.imwrite(str(template_path), template)

    frame = ScreenFrame(source, 60, 60)
    detector = TemplateDetector(tmp_path, confidence=0.9, scales=(1.5,))

    match = detector.find(frame, "scaled.png")

    assert match is not None
    assert match.scale == 1.5
    assert match.x == 25
    assert match.y == 20
