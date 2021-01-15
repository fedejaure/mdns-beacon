"""Tests for `base` module."""
import os
import signal
import threading
import time
from asyncio import AbstractEventLoop
from typing import Optional

import pytest
from pytest_mock import MockerFixture
from zeroconf import IPVersion

from mdns_beacon.base import BaseBeacon


class DummyBeacon(BaseBeacon):
    """Dummy Beacon for testing purpose."""

    def _execute(self) -> None:
        """Execute dummy action."""
        self.zeroconf


@pytest.mark.parametrize(
    "ip_version",
    [
        None,
        IPVersion.V4Only,
        IPVersion.V6Only,
    ],
)
def test_run_forever(
    mocker: MockerFixture, safe_loop: AbstractEventLoop, ip_version: Optional[IPVersion]
) -> None:
    """Test run forever."""

    def _send_signal() -> None:
        time.sleep(0.5)
        os.kill(os.getpid(), signal.SIGINT)

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    beacon = DummyBeacon(ip_version=ip_version)

    with pytest.raises(KeyboardInterrupt):
        beacon.run_forever()
    beacon.stop()

    assert not beacon._zeroconf

    # asserting the loop is stopped but not closed
    assert not safe_loop.is_running()
    assert not safe_loop.is_closed()
    safe_loop.close.assert_called_once_with()  # type: ignore
