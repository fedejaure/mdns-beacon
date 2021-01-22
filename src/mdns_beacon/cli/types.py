"""Param types for mdns-beacon."""
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import AnyStr, Optional, Union

import click


class IpAddress(click.ParamType):
    """An IPv4Address or IPv6Address parsed via ipaddress.ip_address.

    Example:
        >>> ptype = IpAddress()
        >>> ptype.convert("127.0.0.1", None, None)
        IPv4Address('127.0.0.1')
    """

    name = "ip_address"

    def convert(
        self, value: AnyStr, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Union[IPv4Address, IPv6Address]:
        """Parse value into IPv4Address or IPv6Address."""
        try:
            return ip_address(value)
        except ValueError:
            self.fail(f"expected an IPv4 or IPv6 address, got {value!r}", param, ctx)
