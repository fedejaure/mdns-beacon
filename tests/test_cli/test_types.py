"""Tests for `mdns_beacon.cli.types` module."""
from contextlib import ExitStack as does_not_raise
from ipaddress import IPv4Address, IPv6Address
from typing import ContextManager, Optional, Union

import pytest
from click.exceptions import BadParameter

from mdns_beacon.cli.types import IpAddress


@pytest.mark.parametrize(
    "address,raises,expected",
    [
        ("127.0.0.1", does_not_raise(), IPv4Address("127.0.0.1")),
        ("::1", does_not_raise(), IPv6Address("::1")),
        ("wrong address", pytest.raises(BadParameter), None),
    ],
)
def test_ip_address_param_type(
    address: str, raises: ContextManager, expected: Optional[Union[IPv4Address, IPv6Address]]
) -> None:
    """Test ip address param type."""
    ptype = IpAddress()
    with raises:
        ip = ptype.convert(address, None, None)
        assert ip == expected
