"""Conftest module."""
import asyncio
from asyncio import AbstractEventLoop
from typing import Generator

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def safe_loop(
    event_loop: AbstractEventLoop, mocker: MockerFixture
) -> Generator[AbstractEventLoop, None, None]:
    """Safe event loop fixture."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    _close = loop.close
    loop.close = mocker.Mock()  # type: ignore
    yield loop
    _close()
