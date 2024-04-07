"""Tests for `beacon` module."""

from asyncio import AbstractEventLoop
from typing import Any, Dict, Set
from uuid import uuid4

import pytest
from zeroconf import IPVersion

from mdns_beacon.beacon import Beacon

from helpers.contextmanager import raise_keyboard_interrupt


@pytest.mark.slow
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
    safe_loop: AbstractEventLoop,
    beacon_params: Dict[str, Any],
    expected_services: Set[str],
) -> None:
    """Test beacon."""
    # Ugly hack to prevent collisions during parallel tests
    uuid = uuid4()
    beacon_params["aliases"] = [
        a.replace("example", f"example-{uuid}") for a in beacon_params.get("aliases", [])
    ]  # TODO: Fix me
    expected_services = {
        s.replace("example", f"example-{uuid}") for s in expected_services
    }  # TODO: Fix me

    beacon = Beacon(**beacon_params)
    with raise_keyboard_interrupt(timeout=4):
        beacon.run_forever()

    assert expected_services == {s.server for s in beacon.services}

    beacon.stop()

    # asserting the loop is stopped but not closed
    assert not safe_loop.is_running()
    assert not safe_loop.is_closed()
    safe_loop.close.assert_called_once_with()  # type: ignore
