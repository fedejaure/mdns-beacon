"""Console script for mdns-beacon."""
from typing import List, Optional

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
@click.option(
    "--service",
    "services",
    default=None,
    multiple=True,
    help="Service to listen for on the local network.",
)
def listen(services: Optional[List[str]]) -> None:
    """Listen for services on the local network."""
    listerner = BeaconListener(services=list(services), handlers=[on_service_state_change])
    services_msg = (
        ",".join([repr(service) for service in listerner.services])
        if len(listerner.services) < 3
        else f"{len(listerner.services)} services"
    )
    click.echo(f"mdns-beacon listen for {services_msg} (Press CTRL+C to quit)")
    try:
        listerner.run_forever()
    finally:
        listerner.stop()


if __name__ == "__main__":
    main()  # pragma: no cover
