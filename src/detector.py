from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from .screen import ScreenFrame


@dataclass(frozen=True)
class Region:
    """Pixel-space search region: x, y, width, height."""

    x: int
    y: int
    width: int
    height: int

    def clamp(self, frame: ScreenFrame) -> "Region":
        x = max(0, min(self.x, frame.width))
        y = max(0, min(self.y, frame.height))
        right = max(x, min(self.x + self.width, frame.width))
        bottom = max(y, min(self.y + self.height, frame.height))
        return Region(x, y, right - x, bottom - y)


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
    """Resolution-aware multi-scale template detector with optional ROI."""

    DEFAULT_SCALES = (0.60, 0.75, 0.85, 1.0, 1.15, 1.25, 1.40, 1.60)

    def __init__(
        self,
        template_dir: str | Path,
        confidence: float = 0.78,
        scales: tuple[float, ...] | None = None,
        min_margin: float = 0.02,
    ):
        self.template_dir = Path(template_dir)
        self.confidence = confidence
        self.scales = scales or self.DEFAULT_SCALES
        self.min_margin = max(0.0, min_margin)

    @staticmethod
    def _same_location(first: Match, second: Match) -> bool:
        """Treat nearby scale variants as the same physical match."""
        first_center = first.center
        second_center = second.center
        x_limit = max(first.width, second.width) / 2
        y_limit = max(first.height, second.height) / 2
        return (
            abs(first_center[0] - second_center[0]) <= x_limit
            and abs(first_center[1] - second_center[1]) <= y_limit
        )

    def _add_candidate(self, candidates: list[Match], candidate: Match) -> None:
        """Keep the strongest scale for each physical location."""
        for index, existing in enumerate(candidates):
            if self._same_location(existing, candidate):
                if candidate.confidence > existing.confidence:
                    candidates[index] = candidate
                return
        candidates.append(candidate)

    def _scale_candidates(
        self,
        source: np.ndarray,
        template_name: str,
        template: np.ndarray,
        scale: float,
        search: Region,
    ) -> list[Match]:
        width = max(1, int(template.shape[1] * scale))
        height = max(1, int(template.shape[0] * scale))

        if width > source.shape[1] or height > source.shape[0]:
            return []

        interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
        resized = cv2.resize(template, (width, height), interpolation=interpolation)
        result = cv2.matchTemplate(source, resized, cv2.TM_CCOEFF_NORMED)

        kernel_width = max(3, width // 2)
        kernel_height = max(3, height // 2)
        kernel = np.ones((kernel_height, kernel_width), dtype=np.uint8)
        local_max = cv2.dilate(result, kernel)
        peak_mask = (result >= self.confidence) & (
            result >= local_max - 1e-6
        )
        locations = np.argwhere(peak_mask)

        matches: list[Match] = []
        for row, column in locations:
            matches.append(
                Match(
                    template_name,
                    int(column + search.x),
                    int(row + search.y),
                    width,
                    height,
                    float(result[row, column]),
                    scale,
                )
            )

        matches.sort(key=lambda item: item.confidence, reverse=True)
        return matches

    def find(
        self,
        frame: ScreenFrame,
        template_name: str,
        region: Region | None = None,
    ) -> Match | None:
        path = self.template_dir / template_name
        template = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError(f"Template not found: {path}")

        search = region.clamp(frame) if region else Region(0, 0, frame.width, frame.height)
        if search.width <= 0 or search.height <= 0:
            return None

        source = frame.image[
            search.y : search.y + search.height,
            search.x : search.x + search.width,
        ]

        candidates: list[Match] = []

        for scale in self.scales:
            if scale <= 0:
                continue

            for candidate in self._scale_candidates(
                source, template_name, template, scale, search
            ):
                self._add_candidate(candidates, candidate)

        if not candidates:
            return None

        candidates.sort(key=lambda item: item.confidence, reverse=True)
        best = candidates[0]

        if len(candidates) > 1 and (
            best.confidence - candidates[1].confidence < self.min_margin
        ):
            return None

        return best
