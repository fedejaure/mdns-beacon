"""Utils tests module."""
import contextlib
import os
import signal
import threading
import time
from typing import Generator


@contextlib.contextmanager
def raise_keyboard_interrupt(*, timeout: float) -> Generator[None, None, None]:
    """Start a thread that raise a KeyboardInterrupt in `timeout`."""

    def _send_signal() -> None:
        time.sleep(timeout)
        os.kill(os.getpid(), signal.SIGINT)

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    try:
        yield
    except KeyboardInterrupt:
        pass
