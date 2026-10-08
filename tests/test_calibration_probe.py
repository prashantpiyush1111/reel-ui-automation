from pathlib import Path

import cv2
import numpy as np

from src.calibration_probe import CalibrationProbe
from src.screen import ScreenFrame


def test_probe_returns_best_scale(tmp_path: Path):
    template = np.zeros((10, 10, 3), dtype=np.uint8)
    template[2:8, 2:8] = 255

    scaled = cv2.resize(template, (15, 15), interpolation=cv2.INTER_CUBIC)
    source = np.zeros((60, 60, 3), dtype=np.uint8)
    source[20:35, 25:40] = scaled

    path = tmp_path / "marker.png"
    cv2.imwrite(str(path), template)

    frame = ScreenFrame(source, 60, 60)
    probe = CalibrationProbe(tmp_path, scales=(1.0, 1.5))

    result = probe.probe(frame, "marker.png")

    assert result is not None
    assert result.scale == 1.5
    assert result.x == 25
    assert result.y == 20
    assert result.confidence >= 0.9
