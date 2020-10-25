"""Console script for mdns-beacon."""
import click
from zeroconf import ServiceStateChange, Zeroconf

from mdns_beacon import __version__
from mdns_beacon.listener import BeaconListener


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
def listen() -> None:
    """Listen for services on the local network."""
    listerner = BeaconListener(handlers=[on_service_state_change])
    listerner.run_forever()


if __name__ == "__main__":
    main()  # pragma: no cover
