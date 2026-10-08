from dataclasses import dataclass
from pathlib import Path

import cv2

from .screen import ScreenFrame
from .screen import capture_screen


@dataclass(frozen=True)
class CalibrationResult:
    template_name: str
    scale: float
    confidence: float
    x: int
    y: int
    width: int
    height: int


class CalibrationProbe:
    """Measure template-match quality without clicking or changing the UI."""

    def __init__(
        self,
        template_dir: str | Path,
        scales: tuple[float, ...] = (0.60, 0.75, 0.85, 1.0, 1.15, 1.25, 1.40, 1.60),
    ):
        self.template_dir = Path(template_dir)
        self.scales = scales

    def probe(self, frame: ScreenFrame, template_name: str) -> CalibrationResult | None:
        path = self.template_dir / template_name
        template = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError(f"Template not found: {path}")

        best: CalibrationResult | None = None

        for scale in self.scales:
            if scale <= 0:
                continue

            width = max(1, int(template.shape[1] * scale))
            height = max(1, int(template.shape[0] * scale))

            if width >= frame.image.shape[1] or height >= frame.image.shape[0]:
                continue

            interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
            resized = cv2.resize(template, (width, height), interpolation=interpolation)

            result = cv2.matchTemplate(
                frame.image,
                resized,
                cv2.TM_CCOEFF_NORMED,
            )
            _, score, _, location = cv2.minMaxLoc(result)

            candidate = CalibrationResult(
                template_name,
                scale,
                float(score),
                int(location[0]),
                int(location[1]),
                width,
                height,
            )

            if best is None or candidate.confidence > best.confidence:
                best = candidate

        return best


def probe_current_screen(template_dir: str | Path, template_name: str):
    frame = capture_screen()
    return CalibrationProbe(template_dir).probe(frame, template_name)
