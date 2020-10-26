"""Tests for `beacon` module."""
from contextlib import ExitStack as does_not_raise
from typing import Any, ContextManager, Dict

import pytest
from zeroconf import IPVersion

from mdns_beacon.beacon import Beacon


@pytest.mark.parametrize(
    "beacon_params,expected",
    [
        ({}, does_not_raise()),
        (
            {
                "aliases": ["example.local", "sub1.example.local"],
                "ip_version": IPVersion.V4Only,
            },
            does_not_raise(),
        ),
    ],
)
def test_beacon_creation(beacon_params: Dict[str, Any], expected: ContextManager) -> None:
    """Test Beacon creation."""
    with expected:
        Beacon(**beacon_params)
