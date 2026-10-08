import numpy as np
import cv2

from src.detector import TemplateDetector
from src.screen import ScreenFrame


def test_detector_finds_exact_template(tmp_path):
    template = np.zeros((20, 20, 3), dtype=np.uint8)
    template[5:15, 5:15] = 255

    source = np.zeros((80, 100, 3), dtype=np.uint8)
    source[30:50, 40:60] = template

    path = tmp_path / "target.png"
    cv2.imwrite(str(path), template)

    detector = TemplateDetector(tmp_path, confidence=0.95)
    frame = ScreenFrame(source, 100, 80)
    match = detector.find(frame, "target.png")

    assert match is not None
    assert match.confidence >= 0.95
