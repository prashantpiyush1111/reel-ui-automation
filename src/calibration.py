from dataclasses import dataclass


@dataclass(frozen=True)
class Calibration:
    confidence: float
    scale: float


DEFAULT_CALIBRATIONS = (
    Calibration(0.78, 0.75),
    Calibration(0.80, 0.85),
    Calibration(0.82, 1.0),
    Calibration(0.80, 1.15),
    Calibration(0.78, 1.25),
    Calibration(0.76, 1.40),
)


def choose_threshold(scores: list[float]) -> float:
    """Choose a conservative threshold from observed match scores."""
    if not scores:
        return 0.78
    scores = sorted(scores)
    median = scores[len(scores) // 2]
    return max(0.70, min(0.92, median - 0.05))


def rank_calibrations(scores: list[float]) -> tuple[Calibration, ...]:
    """Return scale candidates ordered by observed confidence."""
    if not scores:
        return DEFAULT_CALIBRATIONS

    ranked = sorted(
        zip(DEFAULT_CALIBRATIONS, scores),
        key=lambda item: item[1],
        reverse=True,
    )
    return tuple(calibration for calibration, _ in ranked)
