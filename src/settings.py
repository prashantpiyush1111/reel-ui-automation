import json
from dataclasses import replace
from pathlib import Path

from .config import BotConfig


def load_config(path: str | None = None) -> BotConfig:
    config = BotConfig()
    if not path:
        return config

    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(f"Config file not found: {file}")

    data = json.loads(file.read_text(encoding="utf-8"))
    allowed = {
        "scroll_amount",
        "action_timeout_seconds",
        "retry_delay_seconds",
        "loop_delay_seconds",
        "confidence",
    }
    values = {key: value for key, value in data.items() if key in allowed}
    return replace(config, **values)
