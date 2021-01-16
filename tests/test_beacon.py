"""Tests for `beacon` module."""
import os
import signal
import threading
import time
from asyncio import AbstractEventLoop
from typing import Any, Dict, Set

import pytest
from pytest_mock import MockerFixture
from zeroconf import IPVersion

from mdns_beacon.beacon import Beacon


@pytest.mark.parametrize(
    "beacon_params,expected_services",
    [
        ({}, set()),
        (
            {
                "aliases": ["example", "sub1.example"],
                "ip_version": IPVersion.V4Only,
            },
            {"example.local.", "sub1.example.local."},
        ),
        (
            {
                "aliases": ["example"],
                "ip_version": None,
            },
            {"example.local."},
        ),
        (
            {
                "aliases": ["sub1.example"],
                "ip_version": IPVersion.V6Only,
            },
            {"sub1.example.local."},
        ),
    ],
)
def test_beacon(
    mocker: MockerFixture,
    safe_loop: AbstractEventLoop,
    beacon_params: Dict[str, Any],
    expected_services: Set[str],
) -> None:
    """Test beacon."""

    def _send_signal() -> None:
        time.sleep(2)
        os.kill(os.getpid(), signal.SIGINT)

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    beacon = Beacon(**beacon_params)

    with pytest.raises(KeyboardInterrupt):
        beacon.run_forever()

    assert expected_services == {s.server for s in beacon.services}

    beacon.stop()

    # asserting the loop is stopped but not closed
    assert not safe_loop.is_running()
    assert not safe_loop.is_closed()
    safe_loop.close.assert_called_once_with()  # type: ignore
