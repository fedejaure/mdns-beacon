"""Main module."""
from typing import List, Optional

from zeroconf import IPVersion


class Beacon:
    """mDNS Beacon."""

    def __init__(
        self,
        aliases: Optional[List[str]] = None,
        ip_version: IPVersion = IPVersion.All,
        ttl: int = 60,
    ) -> None:
        """Init a mDNS Beacon instance."""
        self.aliases = aliases or []
        self.ip_version = ip_version
        self.ttl = ttl
