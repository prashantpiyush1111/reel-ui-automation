from pathlib import Path

from .config import BotConfig
from .detector import Match, TemplateDetector
from .screen import capture_screen


class DetectionService:
    def __init__(self, config: BotConfig, template_dir: str | Path | None = None):
        root = Path(__file__).resolve().parent.parent
        resolved_template_dir = (
            Path(template_dir) if template_dir is not None else root / "templates"
        )
        self.detector = TemplateDetector(resolved_template_dir, config.confidence)

    def locate(self, template_name: str) -> Match | None:
        frame = capture_screen()
        return self.detector.find(frame, template_name)
