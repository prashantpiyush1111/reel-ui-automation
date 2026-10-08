from .screen import capture_screen


def print_screen_info() -> None:
    frame = capture_screen()

    import pyautogui

    width, height = pyautogui.size()
    print(f"Screenshot: {frame.width}x{frame.height}")
    print(f"PyAutoGUI:  {width}x{height}")
    if (frame.width, frame.height) != (width, height):
        print("WARNING: screenshot and PyAutoGUI coordinate sizes do not match.")
    else:
        print("Coordinate sizes match.")
