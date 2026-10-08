from dataclasses import dataclass


@dataclass(frozen=True)
class Calibration:
    confidence: float
    scale: float


DEFAULT_CALIBRATIONS = (
    Calibration(0.78, 1.0),
    Calibration(0.82, 1.0),
    Calibration(0.86, 1.0),
)


def choose_threshold(scores: list[float]) -> float:
    """Choose a conservative threshold from observed match scores."""
    if not scores:
        return 0.78
    scores = sorted(scores)
    median = scores[len(scores) // 2]
    return max(0.70, min(0.92, median - 0.05))
