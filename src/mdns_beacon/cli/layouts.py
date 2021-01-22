"""Console layout for mdns-beacon."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from rich.console import RenderableType
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text
from zeroconf import IPVersion, ServiceStateChange, Zeroconf


class BaseLayout(ABC):
    """Base cli layout.

    Note:
        Derived layouts must override the `renderable` property.
    """

    def __init__(self, live: Live) -> None:
        """Init layout."""
        self.live = live
        self.live.update(self.renderable)

    @property
    @abstractmethod
    def renderable(self) -> RenderableType:
        """Get the renderable layout.

        Property that derived layouts must override.
        """


class BlinkLayout(BaseLayout):
    """Blink cli layout."""

    _spinner: Optional[Spinner] = None

    @property
    def spinner(self) -> Spinner:
        """Blink spinner status annimation."""
        if not self._spinner:
            self._spinner = Spinner(
                "dots", text=Text("Announcing services (Press CTRL+C to quit) ...", style="green")
            )
        return self._spinner

    @property
    def renderable(self) -> RenderableType:
        """Blink renderable layout (spinner with status)."""
        layout = Table.grid(padding=1, expand=True)
        layout.add_row(self.spinner)
        return layout


class ListenLayout(BaseLayout):
    """Listen cli layout."""

    services: Dict[str, Any] = {}
    TABLE_SERVICES_COLUMNS = [
        "#",
        "Type",
        "Name",
        "Address IPv4",
        "Port",
        "Server",
        "TTL",
    ]
    _spinner: Optional[Spinner] = None

    @property
    def spinner(self) -> Spinner:
        """Listen spinner status annimation."""
        if not self._spinner:
            self._spinner = Spinner(
                "dots", text=Text("Listen for services (Press CTRL+C to quit) ...", style="green")
            )
        return self._spinner

    @property
    def services_table(self) -> Table:
        """Listen services table."""
        table = Table(expand=True)
        table.title = (
            "\n"
            ":police_car_light::satellite_antenna:"
            " mDNS Beacon Listener "
            ":satellite_antenna::police_car_light:"
        )

        for key in self.TABLE_SERVICES_COLUMNS:
            table.add_column(key, no_wrap=True)

        for index, service in enumerate(self.services.values()):
            table.add_row(
                str(index),
                *[str(v) for k, v in service.items() if k in self.TABLE_SERVICES_COLUMNS],
            )
        return table

    @property
    def renderable(self) -> RenderableType:
        """Listen renderable layout (a table with spinner and status)."""
        layout = Table.grid(padding=1, expand=True)
        layout.add_row(self.services_table)
        layout.add_row(self.spinner)
        return layout

    def update_services(
        self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
    ) -> None:
        """On service state change handler."""
        service_id = f"{name}_{service_type}"
        if state_change is ServiceStateChange.Removed:
            self.services.pop(service_id, None)
        else:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                self.services[service_id] = {
                    "Type": info.type,
                    "Name": info.name,
                    "Address IPv4": ",".join(info.parsed_addresses(IPVersion.V4Only)),
                    "Port": info.port,
                    "Server": info.server,
                    "TTL": info.host_ttl,
                }
        self.live.update(self.renderable)
