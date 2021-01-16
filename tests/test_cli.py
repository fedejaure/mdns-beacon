"""Tests for `mdns_beacon`.cli module."""
from contextlib import ExitStack as does_not_raise
from ipaddress import IPv4Address, IPv6Address
from typing import ContextManager, List, Optional, Union

import pytest
from click.exceptions import BadParameter
from click.testing import CliRunner

import mdns_beacon
from mdns_beacon.cli import IpAddressParamType, main


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "Usage: main [OPTIONS]"),
        (["--help"], "Usage: main [OPTIONS]"),
        (["--version"], f"main, version { mdns_beacon.__version__ }\n"),
    ],
)
def test_command_line_misc(options: List[str], expected: str) -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main, options)
    assert result.exit_code == 0
    assert expected in result.output


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
    ptype = IpAddressParamType()
    with raises:
        ip = ptype.convert(address, None, None)
        assert ip == expected
