"""Tests for `base` module."""
import asyncio
import os
import signal
import threading
import time
from asyncio import AbstractEventLoop
from typing import Generator, Optional

import pytest
from pytest_mock import MockerFixture
from zeroconf import IPVersion

from mdns_beacon.base import BaseBeacon


class DummyBeacon(BaseBeacon):
    """Dummy Beacon for testing purpose."""

    def _execute(self) -> None:
        """Execute dummy action."""
        self.zeroconf


@pytest.fixture
def safe_loop(
    event_loop: AbstractEventLoop, mocker: MockerFixture
) -> Generator[AbstractEventLoop, None, None]:
    """Safe event loop fixture."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    _close = loop.close
    loop.close = mocker.Mock()  # type: ignore
    yield loop
    _close()


@pytest.mark.parametrize(
    "ip_version",
    [
        (None,),
        (IPVersion.V4Only,),
        (IPVersion.V6Only,),
        (IPVersion.All,),
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

    beacon = DummyBeacon()

    with pytest.raises(KeyboardInterrupt):
        beacon.run_forever()
    beacon.stop()

    assert not beacon._zeroconf

    # asserting the loop is stopped but not closed
    assert not safe_loop.is_running()
    assert not safe_loop.is_closed()
    safe_loop.close.assert_called_once_with()  # type: ignore
