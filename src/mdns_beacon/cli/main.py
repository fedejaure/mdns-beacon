"""Main script for mdns-beacon."""
from ipaddress import IPv4Address, IPv6Address
from typing import Dict, Iterable, Tuple, Union

import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup
from rich.console import Console
from rich.live import Live

from mdns_beacon import Beacon, BeaconListener, __version__
from mdns_beacon.beacon import PROTOCOL
from mdns_beacon.cli.layouts import BlinkLayout, ListenLayout
from mdns_beacon.cli.types import IpAddress

console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Simple multicast DNS (mDNS) command line interface utility."""  # noqa:  D401


@main.command()
@click.argument("name")
@click.option(
    "--alias", "aliases", default=[], multiple=True, help="Alias to announce on the local network."
)
@click.option(
    "--address",
    "addresses",
    default=[],
    multiple=True,
    type=IpAddress(),
    help="Address to announce on the local network.",
)
@click.option(
    "--port", "port", default=80, type=int, help="Port to announce on the local network."
)
@click.option("--type", "type_", default="http", type=click.STRING, help="Service type.")
@click.option(
    "--protocol",
    "protocol",
    default="tcp",
    type=click.Choice(choices=("tcp", "udp"), case_sensitive=True),
    help="Service protocol.",
)
@click.option(
    "--weight",
    "weight",
    default=0,
    type=int,
    help="Service weight.",
)
@click.option(
    "--priority",
    "priority",
    default=0,
    type=int,
    help="Service priority.",
)
@optgroup.group(
    "Beacon properties",
    cls=MutuallyExclusiveOptionGroup,
    help="Properties to announce on the local network.",
)
@optgroup.option(
    "--txt",
    "txt",
    type=str,
    callback=lambda ctx, param, value: value.encode("utf8"),
    help="Properties to announce on the local network as `text`.",
    default=b"",
)
@optgroup.option(
    "--property",
    "properties",
    type=click.Tuple([str, str]),
    callback=lambda ctx, param, value: {k.encode("utf8"): v.encode("utf8") for k, v in value},
    help="Properties to announce on the local network (key value).",
    multiple=True,
    default=[],
)
def blink(
    name: str,
    aliases: Iterable[str],
    addresses: Iterable[Union[IPv4Address, IPv6Address]],
    port: int,
    type_: str,
    protocol: PROTOCOL,
    weight: int,
    priority: int,
    txt: bytes,
    properties: Dict[str, bytes],
) -> None:
    """Announce aliases on the local network."""
    with Live(console=console, transient=True, auto_refresh=True) as live:
        BlinkLayout(live=live)
        beacon = Beacon(
            aliases=[name, *aliases],
            addresses=list(addresses),
            port=port,
            type_=type_,
            protocol=protocol,
            weight=weight,
            priority=priority,
            properties=properties or txt,
        )
        try:
            beacon.run_forever()
        except KeyboardInterrupt:
            console.print("Shutting down ...")
        finally:
            beacon.stop()


@main.command()
@click.option(
    "--service",
    "services",
    default=[],
    multiple=True,
    help="Service to listen for on the local network.",
)
@click.option(
    "--show",
    "show_columns",
    type=click.Choice(list(ListenLayout.TABLE_SERVICES_COLUMNS.keys()), case_sensitive=True),
    callback=lambda ctx, param, value: tuple({v: None for v in value}.keys()),
    multiple=True,
    default=ListenLayout.DEFAULT_SHOW_COLUMNS,
    help="Service info to show.",
)
def listen(services: Iterable[str], show_columns: Tuple[str]) -> None:
    """Listen for services on the local network."""
    with Live(console=console, transient=True, auto_refresh=True) as live:
        layout = ListenLayout(live=live, show_columns=show_columns)
        listener = BeaconListener(services=list(services), handlers=[layout.update_services])
        try:
            listener.run_forever()
        except KeyboardInterrupt:
            console.print("Shutting down ...")
        finally:
            listener.stop()


if __name__ == "__main__":
    main()  # pragma: no cover
