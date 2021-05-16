"""Utils tests module."""
import contextlib
import os
import signal
import sys
import threading
import time
from types import FrameType
from typing import Generator, Union


def ctrl_c_event_handler(signum: int, frame: FrameType) -> None:
    """CTRL + C Windows event handler."""
    raise KeyboardInterrupt()


def get_break_signal() -> Union[int, signal.Signals]:
    """Get break signal by platform."""
    if sys.platform == "win32":
        sig = signal.CTRL_C_EVENT
        signal.signal(sig, ctrl_c_event_handler)
        return sig
    return signal.SIGINT


@contextlib.contextmanager
def raise_keyboard_interrupt(*, timeout: float) -> Generator[None, None, None]:
    """Start a thread that raise a KeyboardInterrupt in `timeout`."""

    def _send_signal() -> None:
        time.sleep(timeout)
        os.kill(os.getpid(), get_break_signal())

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    try:
        yield
    except KeyboardInterrupt:
        pass
