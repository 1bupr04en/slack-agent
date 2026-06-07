"""Cross-platform desktop notifications (fallback for workflow errors)."""

import platform
import subprocess
import logging

logger = logging.getLogger(__name__)


def send_notification(title: str, message: str) -> None:
    """Show a desktop notification with given title and message."""
    system = platform.system()

    if system == "Windows":
        try:
            from win10toast import ToastNotifier

            ToastNotifier().show_toast(title, message, duration=5, threaded=True)
            return
        except ImportError:
            logger.warning("win10toast not installed; falling back to log notification")
        except Exception:
            logger.exception("Failed to send Windows notification")
    elif system == "Darwin":
        try:
            subprocess.run([
                "osascript",
                "-e",
                f'display notification "{message}" with title "{title}"',
            ], check=False)
            return
        except Exception:
            logger.exception("Failed to send macOS notification")
    elif system == "Linux":
        try:
            subprocess.run(["notify-send", title, message], check=False)
            return
        except Exception:
            logger.exception("Failed to send Linux notification")

    logger.info("Notification fallback: %s - %s", title, message)
