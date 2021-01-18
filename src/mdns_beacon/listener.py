"""mDNS listener module."""
import logging
from typing import Any, Callable, List, Optional, Set, Union

from zeroconf import ServiceBrowser, ServiceListener, ZeroconfServiceTypes

from .base import BaseBeacon

logger = logging.getLogger(__name__)


class BeaconListener(BaseBeacon):
    """mDNS Beacon listener.

    Attributes:
        handlers: Service listeners or functions to be called when a
            service is added, updated or removed.
        services: Fully qualified service type names list.
        timeout: Seconds to wait for any responses.
    """

    _DEFAULT_SERVICES = {"_http._tcp.local.", "_hap._tcp.local."}

    def __init__(
        self,
        handlers: Union[ServiceListener, List[Callable[..., None]]],
        services: Optional[List[str]] = None,
        timeout: Union[int, float] = 5,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init a mDNS Beacon listener.

        Args:
            handlers: Service listeners or functions to be called when a
                service is added, updated or removed.
            services: Fully qualified service type names list.
            timeout: Seconds to wait for any responses.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.handlers = handlers
        self.timeout = timeout
        self.services = set(services or self.default_services)

    @property
    def default_services(self) -> Set[str]:
        """Return default services to listen on local networks."""
        return self._DEFAULT_SERVICES | set(
            ZeroconfServiceTypes.find(zc=self.zeroconf, timeout=self.timeout)
        )

    def _execute(self) -> None:
        """Listen for services on the local network."""
        logger.debug("Executing beacon listener")
        ServiceBrowser(zc=self.zeroconf, type_=list(self.services), handlers=self.handlers)
