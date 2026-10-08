from dataclasses import dataclass
import sys

import cv2
import numpy as np


_DPI_CONFIGURED = False


def configure_dpi_awareness() -> None:
    """Make Windows screenshot and mouse coordinates use the same DPI space."""
    global _DPI_CONFIGURED

    if _DPI_CONFIGURED or sys.platform != "win32":
        return

    import ctypes

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass

    _DPI_CONFIGURED = True


configure_dpi_awareness()


@dataclass(frozen=True)
class ScreenFrame:
    image: np.ndarray
    width: int
    height: int


def capture_screen() -> ScreenFrame:
    # Import PyAutoGUI only when a real screen capture is requested. This keeps
    # headless CI/test collection independent from an X/GUI display.
    import pyautogui

    shot = pyautogui.screenshot()
    rgb = np.asarray(shot)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    height, width = bgr.shape[:2]
    return ScreenFrame(image=bgr, width=width, height=height)
