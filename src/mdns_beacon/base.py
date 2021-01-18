"""Base mDNS Beacon module."""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional

from zeroconf import IPVersion, Zeroconf

logger = logging.getLogger(__name__)


class BaseBeacon(ABC):
    """mDNS Beacon base class.

    Note:
        Derived beacons must override the `_execute` method.

    Attributes:
        ip_version: IP protocol version to use.
    """

    _zeroconf: Optional[Zeroconf] = None

    def __init__(self, ip_version: Optional[IPVersion] = None) -> None:
        """Init a mDNS Beacon instance.

        Args:
            ip_version: IP protocol version to use.
        """
        self.ip_version = ip_version

    @property
    def zeroconf(self) -> Zeroconf:
        """Zeroconf instance."""
        if not self._zeroconf:
            self._zeroconf = Zeroconf(ip_version=self.ip_version)
        return self._zeroconf

    def stop(self) -> None:
        """Stop Beacon.

        Ends zeroconf background threads, and prevent zeroconf instance from
        servicing further queries.
        """
        logger.debug("Stoping zeroconf")
        self.zeroconf.close()
        self._zeroconf = None

    @abstractmethod
    def _execute(self) -> None:
        """Execute Beacon work.

        Method that derived beacons must override.
        """

    def run_forever(self) -> None:
        """Run beacon forever."""
        self._execute()
        logger.debug("Starting forever loop")
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
