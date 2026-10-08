import logging
from pathlib import Path


def configure_logging() -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/automation.log", encoding="utf-8"),
        ],
    )
    return logging.getLogger("reel_automation")
