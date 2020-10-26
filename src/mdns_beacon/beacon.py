"""Beacon module."""
import logging
import socket
from typing import Any, List, Optional

from zeroconf import ServiceInfo

from .base import BaseBeacon

logger = logging.getLogger(__name__)


class Beacon(BaseBeacon):
    """mDNS Beacon."""

    def __init__(
        self,
        aliases: Optional[List[str]] = None,
        addresses: Optional[List[bytes]] = None,
        port: int = 80,
        type_: str = "http",
        protocol: str = "tcp",
        ttl: int = 60,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init a mDNS Beacon instance."""
        super().__init__(*args, **kwargs)
        self.aliases = aliases or []
        self.addresses = addresses or [socket.inet_aton("127.0.0.1")]
        self.port = port
        self.type_ = type_
        self.protocol = protocol
        self.ttl = ttl

    @property
    def services(self) -> List[ServiceInfo]:
        """Services to register on the local network."""
        return [
            ServiceInfo(
                type_=f"_{self.type_}._{self.protocol}.local.",
                name=f"{alias}._{self.type_}._{self.protocol}.local."
                if "." not in alias
                else f"{alias}._sub._{self.type_}._{self.protocol}.local.",
                addresses=self.addresses,
                port=self.port,
                host_ttl=self.ttl,
                server=f"{alias}.local.",
            )
            for alias in self.aliases
        ]

    def stop(self) -> None:
        """Stop the Beacon."""
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
