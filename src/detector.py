from dataclasses import dataclass
from pathlib import Path

import cv2

from .screen import ScreenFrame


@dataclass(frozen=True)
class Match:
    name: str
    x: int
    y: int
    width: int
    height: int
    confidence: float
    scale: float = 1.0

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)


class TemplateDetector:
    """Resolution-aware multi-scale template detector."""

    DEFAULT_SCALES = (0.60, 0.75, 0.85, 1.0, 1.15, 1.25, 1.40, 1.60)

    def __init__(
        self,
        template_dir: str | Path,
        confidence: float = 0.78,
        scales: tuple[float, ...] | None = None,
    ):
        self.template_dir = Path(template_dir)
        self.confidence = confidence
        self.scales = scales or self.DEFAULT_SCALES

    def find(self, frame: ScreenFrame, template_name: str) -> Match | None:
        path = self.template_dir / template_name
        template = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError(f"Template not found: {path}")

        source = frame.image
        best: Match | None = None

        for scale in self.scales:
            if scale <= 0:
                continue

            width = max(1, int(template.shape[1] * scale))
            height = max(1, int(template.shape[0] * scale))

            if width >= source.shape[1] or height >= source.shape[0]:
                continue

            interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
            resized = cv2.resize(template, (width, height), interpolation=interpolation)

            result = cv2.matchTemplate(source, resized, cv2.TM_CCOEFF_NORMED)
            _, score, _, location = cv2.minMaxLoc(result)

            if score < self.confidence:
                continue

            candidate = Match(
                template_name,
                int(location[0]),
                int(location[1]),
                width,
                height,
                float(score),
                scale,
            )

            if best is None or candidate.confidence > best.confidence:
                best = candidate

        return best
