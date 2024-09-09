"""Tests for `base` module."""

from asyncio import AbstractEventLoop
from typing import Optional

import pytest
from zeroconf import IPVersion

from mdns_beacon.base import BaseBeacon

from helpers.contextmanager import raise_keyboard_interrupt


class DummyBeacon(BaseBeacon):
    """Dummy Beacon for testing purpose."""

    def _execute(self) -> None:
        """Execute dummy action."""


@pytest.mark.parametrize(
    "ip_version",
    [
        None,
        IPVersion.V4Only,
        IPVersion.V6Only,
    ],
)
def test_run_forever(safe_loop: AbstractEventLoop, ip_version: Optional[IPVersion]) -> None:
    """Test run forever."""
    beacon = DummyBeacon(ip_version=ip_version)

    with raise_keyboard_interrupt(timeout=0.5):
        beacon.run_forever()
    beacon.stop()

    assert not beacon._zeroconf

    # asserting the loop is stopped but not closed
    assert not safe_loop.is_running()
    assert not safe_loop.is_closed()
    safe_loop.close.assert_called_once_with()  # type: ignore
