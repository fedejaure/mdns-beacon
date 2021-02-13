"""Beacon module."""
import logging
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Any, Dict, List, Optional, Union

from slugify import slugify
from typing_extensions import Literal
from zeroconf import ServiceInfo

from .base import BaseBeacon

logger = logging.getLogger(__name__)

PROTOCOL = Literal["tcp", "udp"]


class Beacon(BaseBeacon):
    """mDNS Beacon.

    Attributes:
        aliases: Service alias name list.
        addresses: IP addresses that the service runs on.
        port: Port that the service runs on.
        type_: Service type.
        protocol: Service protocol.
        ttl: TTL used for the announce of the service.
        weight: Weight of the service.
        priority: Priority of the service.
        properties: Dict of properties (or a bytes object with the content of the `text` field).
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    _SLUG_REGEX_PATTERN = r"[^-a-z0-9_.]+"
    _SLUG_SEPARATOR = "-"
    _services: Optional[List[ServiceInfo]] = None

    def __init__(
        self,
        aliases: Optional[List[str]] = None,
        addresses: Optional[List[Union[IPv4Address, IPv6Address]]] = None,
        port: int = 80,
        type_: str = "http",
        protocol: PROTOCOL = "tcp",
        ttl: int = 60,
        weight: int = 0,
        priority: int = 0,
        properties: Union[bytes, Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init a mDNS Beacon instance.

        Args:
            aliases: Service alias name list.
            addresses: IP addresses that the service runs on.
            port: Port that the service runs on.
            type_: Service type.
            protocol: Service protocol.
            ttl: TTL used for the announce of the service.
            weight: Weight of the service.
            priority: Priority of the service.
            properties: Dict of properties (or a bytes object with the
                content of the `text` field) of the service.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.aliases = set(aliases or [])
        self.addresses = set(addresses or [ip_address("127.0.0.1")])
        self.port = port
        self.type_ = type_
        self.protocol = protocol
        self.ttl = ttl
        self.weight = weight
        self.priority = priority
        self.properties = properties or b""

    def _build_service_host(self, name: str) -> str:
        """Build service host for a given name.

        Args:
            name: Service name.

        Returns:
            Fully qualified service host name.
        """
        slug = slugify(
            name, separator=self._SLUG_SEPARATOR, regex_pattern=self._SLUG_REGEX_PATTERN
        )
        return f"{slug}.local."

    def _build_service_name(self, name: str) -> str:
        """Build service name for a given name.

        Args:
            name: Service name.

        Returns:
            Fully qualified service name.
        """
        return f"{name}.{self.service_type}"

    @property
    def service_type(self) -> str:
        """Beacon service type."""
        return f"_{self.type_}._{self.protocol}.local."

    @property
    def services(self) -> List[ServiceInfo]:
        """Services to register on the local network."""
        if not self._services:
            self._services = [
                ServiceInfo(
                    type_=self.service_type,
                    name=self._build_service_name(alias),
                    parsed_addresses=[str(addr) for addr in self.addresses],
                    port=self.port,
                    host_ttl=self.ttl,
                    weight=self.weight,
                    priority=self.priority,
                    properties=self.properties,
                    server=self._build_service_host(alias),
                )
                for alias in self.aliases
            ]
        return self._services

    def stop(self) -> None:
        """Stop Beacon.

        Unregister all the announced services.
        """
        logger.info("Unregistering %(services_len)s services", services_len=len(self.services))
        for service in self.services:
            logger.debug("Unregistering %(service_name)s", service_name=service.name)
            self.zeroconf.unregister_service(service)
        super().stop()

    def _execute(self) -> None:
        """Register aliases on the local network."""
        logger.info("Registering %(services_len)s services", services_len=len(self.services))
        for service in self.services:
            logger.debug("Registering %(service_name)s", service_name=service.name)
            self.zeroconf.register_service(service)
