"""Tests for `mdns_beacon`.cli module."""
from click.testing import CliRunner

import mdns_beacon
from mdns_beacon import cli


def test_command_line_interface() -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS]" in result.output


def test_command_line_interface_help() -> None:
    """Test the CLI help option."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Usage: main [OPTIONS]" in help_result.output


def test_command_line_interface_version() -> None:
    """Test the CLI version option."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ["--version"])
    assert help_result.exit_code == 0
    assert f"main, version { mdns_beacon.__version__ }\n" == help_result.output
