from _bootstrap import REPO_ROOT

from src.config import BotConfig
from src.dry_run import DryRun
from src.logger import configure_logging


if __name__ == "__main__":
    configure_logging()
    states = DryRun(BotConfig()).execute()
    print("Dry run completed:")
    print(" -> ".join(states))
