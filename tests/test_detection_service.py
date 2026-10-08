from pathlib import Path

from src.config import BotConfig
from src.detection_service import DetectionService


def test_detection_service_uses_repo_root_templates_by_default():
    service = DetectionService(BotConfig())
    expected = Path(__file__).resolve().parents[1] / "templates"

    assert service.detector.template_dir == expected
