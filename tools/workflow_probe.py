import argparse

from src.config import BotConfig
from src.logger import configure_logging
from src.step_runner import StepRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe one UI workflow step.")
    parser.add_argument("step", choices=("detect", "open-comments", "next"))
    args = parser.parse_args()

    configure_logging()
    runner = StepRunner(BotConfig())

    if args.step == "detect":
        print("Reel detected." if runner.detect_reel() else "Reel not detected.")
    elif args.step == "open-comments":
        print("Comment panel opened." if runner.open_comments() else "Comment panel not opened.")
    else:
        runner.next_reel()
        print("Moved to next Reel.")


if __name__ == "__main__":
    main()
