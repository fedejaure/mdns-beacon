"""Console script for mdns-beacon."""
from typing import List

import click
from zeroconf import ServiceStateChange, Zeroconf

from mdns_beacon import Beacon, BeaconListener, __version__


def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    """On service state change handler."""
    click.echo(f"Service {name} of type {service_type} state changed: {state_change}")


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Simple multicast DNS (mDNS) client line interface utility."""  # noqa:  D401


@main.command()
@click.argument("name")
@click.option(
    "--alias", "aliases", default=[], multiple=True, help="Alias to announce on the local network."
)
def blink(name: str, aliases: List[str]) -> None:
    """Announce aliases on the local network."""
    beacon = Beacon(aliases=[name, *aliases])
    try:
        beacon.run_forever()
    finally:
        beacon.stop()


@main.command()
def listen() -> None:
    """Listen for services on the local network."""
    listerner = BeaconListener(handlers=[on_service_state_change])
    try:
        listerner.run_forever()
    finally:
        listerner.stop()


if __name__ == "__main__":
    main()  # pragma: no cover
