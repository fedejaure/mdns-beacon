"""Tests for `listener` module."""
import os
import signal
import threading
import time
from asyncio import AbstractEventLoop
from typing import List, Optional, Union

import pytest
from pytest_mock import MockerFixture
from zeroconf import IPVersion, ServiceStateChange, Zeroconf

from mdns_beacon.listener import BeaconListener


@pytest.mark.parametrize(
    "ip_version,services,timeout",
    [
        (None, None, 2),
        (IPVersion.V4Only, None, 2),
        (IPVersion.V6Only, None, 2),
        (None, ["_http._tcp.local."], 0.5),
        (IPVersion.V4Only, ["_http._tcp.local."], 0.5),
        (IPVersion.V6Only, ["_http._tcp.local."], 0.5),
    ],
)
def test_beacon_listener(
    mocker: MockerFixture,
    safe_loop: AbstractEventLoop,
    ip_version: Optional[IPVersion],
    services: Optional[List[str]],
    timeout: Union[int, float],
) -> None:
    """Test beacon listener."""

    def _send_signal() -> None:
        time.sleep(timeout + 0.5)
        os.kill(os.getpid(), signal.SIGINT)

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    def _on_service_state_change(
        zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
    ) -> None:
        pass

    listener = BeaconListener(
        ip_version=ip_version,
        handlers=[_on_service_state_change],
        services=services,
        timeout=timeout,
    )

    with pytest.raises(KeyboardInterrupt):
        listener.run_forever()
    listener.stop()
