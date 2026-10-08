import time

from .config import BotConfig
from .controller import SafeController


def run() -> None:
    config = BotConfig()
    controller = SafeController(config)

    print("Reel UI Automation started.")
    print("Press Ctrl+C to stop.")

    try:
        while not controller.stopped:
            controller.wait_if_paused()
            if controller.stopped:
                break

            # Detection and workflow states will be added incrementally.
            controller.scroll_next()
            time.sleep(config.loop_delay_seconds)
    except KeyboardInterrupt:
        controller.stop()
        print("Stopped safely.")


if __name__ == "__main__":
    run()
