from src.config import BotConfig


def test_default_config_is_safe():
    config = BotConfig()
    assert config.confidence > 0
    assert config.action_timeout_seconds > 0
    assert config.retry_delay_seconds > 0
