from .config import BotConfig
from .detector import Match, TemplateDetector
from .screen import capture_screen


class DetectionService:
    def __init__(self, config: BotConfig, template_dir: str = "templates"):
        self.detector = TemplateDetector(template_dir, config.confidence)

    def locate(self, template_name: str) -> Match | None:
        frame = capture_screen()
        return self.detector.find(frame, template_name)
