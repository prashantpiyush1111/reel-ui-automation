from src.calibration import choose_threshold


def test_threshold_stays_in_safe_range():
    assert 0.70 <= choose_threshold([0.9, 0.91, 0.92]) <= 0.92


def test_empty_scores_use_default():
    assert choose_threshold([]) == 0.78
