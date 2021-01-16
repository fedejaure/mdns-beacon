"""mDNS listener module."""
import logging
from typing import Any, Callable, List, Optional, Set, Union

from zeroconf import ServiceBrowser, ServiceListener, ZeroconfServiceTypes

from .base import BaseBeacon

logger = logging.getLogger(__name__)


class BeaconListener(BaseBeacon):
    """mDNS Beacon listener."""

    _DEFAULT_SERVICES = {"_http._tcp.local.", "_hap._tcp.local."}

    def __init__(
        self,
        handlers: Union[ServiceListener, List[Callable[..., None]]],
        services: Optional[List[str]] = None,
        timeout: Union[int, float] = 5,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init a mDNS Beacon listener."""
        super().__init__(*args, **kwargs)
        self.handlers = handlers
        self.timeout = timeout
        self.services = set(services or self.default_services)

    @property
    def default_services(self) -> Set[str]:
        """Find default services."""
        return self._DEFAULT_SERVICES | set(
            ZeroconfServiceTypes.find(zc=self.zeroconf, timeout=self.timeout)
        )

    def _execute(self) -> None:
        """Listen for services on the local network."""
        logger.debug("Executing beacon listener")
        ServiceBrowser(zc=self.zeroconf, type_=list(self.services), handlers=self.handlers)
