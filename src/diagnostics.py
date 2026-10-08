from .screen import capture_screen


def print_screen_info() -> None:
    frame = capture_screen()
    print(f"Screen: {frame.width}x{frame.height}")
