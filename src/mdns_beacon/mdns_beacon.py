"""Main module."""
from typing import List, Optional

from zeroconf import IPVersion


class Beacon:
    """mDNS Beacon."""

    def __init__(
        self, aliases: List[str], ip_version: IPVersion = IPVersion.All, ttl: Optional[int] = 60
    ) -> None:
        """Init a mDNS Beacon instance."""
        self.aliases = aliases
        self.ip_version = ip_version
