"""Tests for `listener` module."""

from asyncio import AbstractEventLoop
from typing import Any, Dict, Set

import pytest
from zeroconf import IPVersion

from mdns_beacon.listener import BeaconListener

from helpers.contextmanager import raise_keyboard_interrupt


@pytest.mark.slow
@pytest.mark.parametrize(
    "beacon_params,expected_services",
    [
        ({"ip_version": None, "services": None, "timeout": 2}, BeaconListener._DEFAULT_SERVICES),
        (
            {"ip_version": IPVersion.V4Only, "services": None, "timeout": 2},
            BeaconListener._DEFAULT_SERVICES,
        ),
        (
            {"ip_version": IPVersion.V6Only, "services": None, "timeout": 2},
            BeaconListener._DEFAULT_SERVICES,
        ),
        (
            {
                "ip_version": None,
                "services": ["_http._tcp.local.", "_http._tcp.local."],
                "timeout": 0.5,
            },
            {"_http._tcp.local."},
        ),
        (
            {"ip_version": IPVersion.V4Only, "services": ["_hap._tcp.local."], "timeout": 0.5},
            {"_hap._tcp.local."},
        ),
        (
            {
                "ip_version": IPVersion.V6Only,
                "services": ["_some_type._some_protocol.local."],
                "timeout": 1,
            },
            {"_some_type._some_protocol.local."},
        ),
    ],
)
def test_beacon_listener(
    safe_loop: AbstractEventLoop,
    beacon_params: Dict[str, Any],
    expected_services: Set[str],
) -> None:
    """Test beacon listener."""
    listener = BeaconListener(
        handlers=[lambda *args, **kwargs: None],
        **beacon_params,
    )

    with raise_keyboard_interrupt(timeout=beacon_params["timeout"] + 1):
        listener.run_forever()

    assert expected_services.issubset(listener.services)

    listener.stop()

    # asserting the loop is stopped but not closed
    assert not safe_loop.is_running()
    assert not safe_loop.is_closed()
    safe_loop.close.assert_called_once_with()  # type: ignore
