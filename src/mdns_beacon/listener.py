"""mDNS listener module."""
import logging
from typing import Any, Callable, List, Optional, Union

from zeroconf import ServiceBrowser, ServiceListener, ZeroconfServiceTypes

from .base import BaseBeacon

logger = logging.getLogger(__name__)


class BeaconListener(BaseBeacon):
    """mDNS Beacon listener."""

    def __init__(
        self,
        handlers: Union[ServiceListener, List[Callable[..., None]]],
        services: Optional[List[str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init a mDNS Beacon listener."""
        super().__init__(*args, **kwargs)
        self.handlers = handlers
        self.services = services or list(ZeroconfServiceTypes.find(zc=self.zeroconf))

    def _execute(self) -> None:
        """Listen for services on the local network."""
        ServiceBrowser(zc=self.zeroconf, type_=self.services, handlers=self.handlers)
