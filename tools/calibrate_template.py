import argparse

from _bootstrap import REPO_ROOT

from src.calibration_probe import probe_current_screen


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure template scale/confidence on the current screen."
    )
    parser.add_argument("template", help="Template filename inside templates/")
    args = parser.parse_args()

    try:
        result = probe_current_screen(REPO_ROOT / "templates", args.template)
    except FileNotFoundError as exc:
        print(exc)
        return 1

    if result is None:
        print("No valid scale candidate could be evaluated.")
        return 1

    print(f"Template:   {result.template_name}")
    print(f"Scale:      {result.scale:.2f}x")
    print(f"Confidence: {result.confidence:.4f}")
    print(f"Position:   ({result.x}, {result.y})")
    print(f"Size:       {result.width}x{result.height}")

    if result.confidence >= 0.85:
        print("Assessment: strong match")
    elif result.confidence >= 0.78:
        print("Assessment: usable match")
    else:
        print("Assessment: weak match; recapture or recalibrate the template")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
