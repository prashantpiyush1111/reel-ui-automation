from dataclasses import dataclass, field


@dataclass(frozen=True)
class BotConfig:
    scroll_amount: int = -6
    action_timeout_seconds: float = 5.0
    retry_delay_seconds: float = 0.35
    loop_delay_seconds: float = 1.0
    confidence: float = 0.78
    comments: tuple[str, ...] = field(default_factory=tuple)
