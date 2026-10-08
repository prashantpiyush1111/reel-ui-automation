from pathlib import Path

import pyautogui


def main() -> None:
    output = Path("templates")
    output.mkdir(exist_ok=True)

    name = input("Template filename (for example comment_button.png): ").strip()
    if not name:
        raise SystemExit("A filename is required.")

    if not name.lower().endswith(".png"):
        name += ".png"

    print("Move the mouse to the top-left corner of the target area.")
    input("Press Enter when ready...")
    x1, y1 = pyautogui.position()

    print("Move the mouse to the bottom-right corner of the target area.")
    input("Press Enter when ready...")
    x2, y2 = pyautogui.position()

    if x2 <= x1 or y2 <= y1:
        raise SystemExit("Invalid capture area.")

    image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    path = output / name
    image.save(path)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
