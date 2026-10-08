from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2


@dataclass(frozen=True)
class TemplateInfo:
    name: str
    width: int
    height: int
    channels: int


def inspect_template(path: Path) -> TemplateInfo:
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Unable to read template: {path}")

    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else image.shape[2]
    if width < 8 or height < 8:
        raise ValueError(f"Template is too small: {path.name}")

    return TemplateInfo(path.name, width, height, channels)


def validate_templates(template_dir: Path, required: tuple[str, ...]) -> list[str]:
    errors: list[str] = []

    for name in required:
        path = template_dir / name
        if not path.exists():
            errors.append(f"Missing template: {name}")
            continue

        try:
            info = inspect_template(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if info.width > 1000 or info.height > 1000:
            errors.append(
                f"Template is unusually large ({info.width}x{info.height}): {name}"
            )

    return errors
