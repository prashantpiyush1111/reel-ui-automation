import argparse

from src.config import BotConfig
from src.detection_service import DetectionService
from src.logger import configure_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe a UI template on the current screen.")
    parser.add_argument("template", help="Template filename inside templates/")
    args = parser.parse_args()

    configure_logging()
    detector = DetectionService(BotConfig())
    match = detector.locate(args.template)

    if match is None:
        print(f"NOT FOUND: {args.template}")
        raise SystemExit(2)

    print(f"FOUND: {match.name}")
    print(f"Position: ({match.x}, {match.y})")
    print(f"Size: {match.width}x{match.height}")
    print(f"Center: {match.center}")
    print(f"Confidence: {match.confidence:.3f}")


if __name__ == "__main__":
    main()
