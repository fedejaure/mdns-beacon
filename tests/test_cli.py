"""Tests for `mdns_beacon`.cli module."""
from asyncio import AbstractEventLoop
from contextlib import ExitStack as does_not_raise
from ipaddress import IPv4Address, IPv6Address
from typing import ContextManager, List, Optional, Union
from uuid import uuid4

import pytest
from click.exceptions import BadParameter
from click.testing import CliRunner
from pytest_mock import MockerFixture

import mdns_beacon
from mdns_beacon.cli.main import main
from mdns_beacon.cli.types import IpAddress

from helpers.contextmanager import raise_keyboard_interrupt


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "Usage: main [OPTIONS]"),
        (["--help"], "Usage: main [OPTIONS]"),
        (["--version"], f"main, version { mdns_beacon.__version__ }\n"),
    ],
)
def test_command_line_interface(options: List[str], expected: str) -> None:
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
    ptype = IpAddress()
    with raises:
        ip = ptype.convert(address, None, None)
        assert ip == expected


@pytest.mark.slow
@pytest.mark.parametrize(
    "options,expected",
    [
        (["example", "--protocol", "tcp"], "Shutting down ...\n"),
        (["example", "--alias", "sub1.example"], "Shutting down ...\n"),
        (
            ["example", "--alias", "sub1.example", "--address", "127.0.0.1", "--type", "http"],
            "Shutting down ...\n",
        ),
        (
            ["example", "--alias", "sub1.example", "--address", "127.0.0.1", "--address", "::1"],
            "Shutting down ...\n",
        ),
    ],
)
def test_blink(
    mocker: MockerFixture, safe_loop: AbstractEventLoop, options: List[str], expected: str
) -> None:
    """Test beacon blink."""
    # Ugly hack to prevent collisions during parallel tests
    uuid = uuid4()
    options = [opt.replace("example", f"example-{uuid}") for opt in options]  # TODO: Fix me

    runner = CliRunner()
    with raise_keyboard_interrupt(timeout=6):
        result = runner.invoke(main, ["blink"] + options)

    assert result.exit_code == 0
    assert expected in result.output


@pytest.mark.slow
@pytest.mark.parametrize(
    "options,timeout,expected",
    [
        ([], 8, "Shutting down ...\n"),
        (["--service", "_http._tcp.local."], 2, "Shutting down ...\n"),
        (
            ["--service", "_http._tcp.local.", "--service", "_hap._tcp.local."],
            2,
            "Shutting down ...\n",
        ),
    ],
)
def test_listen(
    mocker: MockerFixture,
    safe_loop: AbstractEventLoop,
    options: List[str],
    timeout: float,
    expected: str,
) -> None:
    """Test beacon listen."""
    runner = CliRunner()

    with raise_keyboard_interrupt(timeout=timeout):
        result = runner.invoke(main, ["listen"] + options)

    assert result.exit_code == 0
    assert expected in result.output
