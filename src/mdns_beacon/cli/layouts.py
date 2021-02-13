"""Console layout for mdns-beacon."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

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

    _spinner: Optional[Spinner] = None

    def __init__(self, live: Live) -> None:
        """Init layout."""
        self.live = live
        self.live.update(self.renderable)

    @property
    @abstractmethod
    def spinner_text(self) -> str:
        """Get the spinner text to render.

        Property that derived layouts must override.
        """

    @property
    def spinner(self) -> Spinner:
        """Spinner status annimation."""
        if not self._spinner:
            self._spinner = Spinner("dots", text=Text(self.spinner_text, style="green"))
        return self._spinner

    @property
    @abstractmethod
    def renderable(self) -> RenderableType:
        """Get the renderable layout.

        Property that derived layouts must override.
        """


class BlinkLayout(BaseLayout):
    """Blink cli layout."""

    spinner_text = "Announcing services (Press CTRL+C to quit) ..."

    @property
    def renderable(self) -> Table:
        """Blink renderable layout (spinner with status)."""
        layout = Table.grid(padding=1, expand=True)
        layout.add_row(self.spinner)
        return layout


class ListenLayout(BaseLayout):
    """Listen cli layout."""

    services: Dict[str, Any] = {}
    TABLE_SERVICES_COLUMNS = {
        "type": "Type",
        "name": "Name",
        "ipv4_address": "Address IPv4",
        "ipv6_address": "Address IPv6",
        "port": "Port",
        "server": "Server",
        "ttl": "TTL",
        "weight": "Weight",
        "priority": "Priority",
        "text": "TXT",
        "properties": "Properties",
    }
    DEFAULT_SHOW_COLUMNS = (
        "type",
        "name",
        "ipv4_address",
        "port",
        "server",
        "ttl",
    )

    spinner_text = "Listen for services (Press CTRL+C to quit) ..."

    def __init__(
        self,
        show_columns: Optional[Union[Tuple[str], List[str]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init listen layout."""
        self.show_columns = show_columns or self.DEFAULT_SHOW_COLUMNS
        if not set(self.show_columns).issubset(self.TABLE_SERVICES_COLUMNS.keys()):
            raise ValueError(
                "Unknown fields %s", set(self.show_columns) - self.TABLE_SERVICES_COLUMNS.keys()
            )
        super().__init__(*args, **kwargs)

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

        table.add_column("#", no_wrap=True)
        for c in self.show_columns:
            table.add_column(self.TABLE_SERVICES_COLUMNS[c], no_wrap=True)

        for index, service in enumerate(self.services.values()):
            table.add_row(str(index), *[str(service[c]) for c in self.show_columns])
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
                    "type": info.type,
                    "name": info.name,
                    "ipv4_address": ",".join(info.parsed_addresses(IPVersion.V4Only)),
                    "ipv6_address": ",".join(info.parsed_addresses(IPVersion.V6Only)),
                    "port": info.port,
                    "server": info.server,
                    "ttl": info.host_ttl,
                    "weight": info.weight,
                    "priority": info.priority,
                    "text": info.text.decode("utf8"),
                    "properties": {
                        k.decode("utf8"): v.decode("utf8") for k, v in info.properties.items()
                    },
                }
        self.live.update(self.renderable)
