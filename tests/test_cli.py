"""Tests for `mdns_beacon`.cli module."""
import os
import signal
import threading
import time
from asyncio import AbstractEventLoop
from contextlib import ExitStack as does_not_raise
from ipaddress import IPv4Address, IPv6Address
from typing import ContextManager, List, Optional, Union

import pytest
from click.exceptions import BadParameter
from click.testing import CliRunner
from pytest_mock import MockerFixture

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


@pytest.mark.slow
@pytest.mark.parametrize(
    "options,expected",
    [
        (["example"], "Shutting down ...\n"),
        (["example", "--alias", "sub1.example"], "Shutting down ...\n"),
        (["example", "--alias", "sub1.example", "--address", "127.0.0.1"], "Shutting down ...\n"),
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
    runner = CliRunner()

    def _send_signal() -> None:
        time.sleep(2)
        os.kill(os.getpid(), signal.SIGINT)

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    result = runner.invoke(main, ["blink"] + options)

    assert result.exit_code == 0
    assert expected in result.output
