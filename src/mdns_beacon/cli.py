"""Console script for mdns-beacon."""
from typing import Any, Dict, Iterable

import click
from rich.console import Console
from rich.table import Table
from zeroconf import IPVersion, ServiceStateChange, Zeroconf

from mdns_beacon import Beacon, BeaconListener, __version__

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
    """Simple multicast DNS (mDNS) client line interface utility."""  # noqa:  D401


@main.command()
@click.argument("name")
@click.option(
    "--alias", "aliases", default=[], multiple=True, help="Alias to announce on the local network."
)
def blink(name: str, aliases: Iterable[str]) -> None:
    """Announce aliases on the local network."""
    beacon = Beacon(aliases=[name, *aliases])
    try:
        beacon.run_forever()
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
                # "Properties": info.properties,
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
    listerner = BeaconListener(services=list(services), handlers=[on_service_state_change])
    try:
        listerner.run_forever()
    finally:
        console.clear()
        listerner.stop()


if __name__ == "__main__":
    main()  # pragma: no cover
