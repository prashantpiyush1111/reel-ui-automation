from src.config import BotConfig
from src.dry_run import DryRun


def test_dry_run_visits_expected_states():
    states = DryRun(BotConfig()).execute()
    assert states[0] == "WAITING_FOR_REEL"
    assert "READY_FOR_MANUAL_POST" in states
    assert states[-1] == "NEXT_REEL"
