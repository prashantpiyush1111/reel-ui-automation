from dataclasses import dataclass

import cv2
import numpy as np


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
