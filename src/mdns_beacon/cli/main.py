"""Console script for mdns-beacon."""
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Dict, Iterable, Union

import click
from rich.console import Console
from rich.table import Table
from zeroconf import IPVersion, ServiceStateChange, Zeroconf

from mdns_beacon import Beacon, BeaconListener, __version__
from mdns_beacon.beacon import PROTOCOL
from mdns_beacon.cli.types import IpAddress

console = Console()

mDNS_services: Dict[str, Any] = {}
TABLE_SERVICES_COLUMNS = [
    "#",
    "Type",
    "Name",
    "Address IPv4",
    "Port",
    "Server",
    "TTL",
]


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
def blink(
    name: str,
    aliases: Iterable[str],
    addresses: Iterable[Union[IPv4Address, IPv6Address]],
    port: int,
    type_: str,
    protocol: PROTOCOL,
) -> None:
    """Announce aliases on the local network."""
    beacon = Beacon(
        aliases=[name, *aliases],
        addresses=list(addresses),
        port=port,
        type_=type_,
        protocol=protocol,
    )
    try:
        beacon.run_forever()
    except KeyboardInterrupt:
        console.print("Shutting down ...")
    finally:
        beacon.stop()


def print_services() -> None:
    """Print services."""
    console.clear()
    table = Table()
    table.width = console.width
    table.title = (
        ":police_car_light::satellite_antenna:"
        " mDNS Beacon Listener "
        ":satellite_antenna::police_car_light:"
    )

    for key in TABLE_SERVICES_COLUMNS:
        table.add_column(key, no_wrap=True)

    for index, service in enumerate(mDNS_services.values()):
        table.add_row(
            str(index), *[str(v) for k, v in service.items() if k in TABLE_SERVICES_COLUMNS]
        )

    console.print(table, justify="center")
    console.print("Listen for services (Press CTRL+C to quit) ...")


def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    """On service state change handler."""
    global mDNS_services
    service_id = f"{name}_{service_type}"
    if state_change is ServiceStateChange.Removed:
        mDNS_services.pop(service_id, None)
    else:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            mDNS_services[service_id] = {
                "Type": info.type,
                "Name": info.name,
                "Address IPv4": ",".join(info.parsed_addresses(IPVersion.V4Only)),
                "Port": info.port,
                "Server": info.server,
                "TTL": info.host_ttl,
            }
    print_services()


@main.command()
@click.option(
    "--service",
    "services",
    default=[],
    multiple=True,
    help="Service to listen for on the local network.",
)
def listen(services: Iterable[str]) -> None:
    """Listen for services on the local network."""
    print_services()
    listener = BeaconListener(services=list(services), handlers=[on_service_state_change])
    try:
        listener.run_forever()
    except KeyboardInterrupt:
        console.print("Shutting down ...")
    finally:
        listener.stop()


if __name__ == "__main__":
    main()  # pragma: no cover