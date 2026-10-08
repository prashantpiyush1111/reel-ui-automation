import importlib

from _bootstrap import REPO_ROOT


REQUIRED = ("cv2", "pyautogui", "PIL", "numpy", "keyboard", "pyperclip")


def main() -> None:
    missing = []
    for module in REQUIRED:
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(module)

    if missing:
        print("Missing dependencies:", ", ".join(missing))
        print("Run: pip install -r requirements.txt")
        raise SystemExit(1)

    print("Python dependencies: OK")
    print(f"Repository root: {REPO_ROOT}")
    print("Environment is ready for the next UI test stage.")


if __name__ == "__main__":
    main()
