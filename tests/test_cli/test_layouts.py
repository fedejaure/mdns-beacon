"""Tests for `mdns_beacon.cli.layouts` module."""

from contextlib import ExitStack as does_not_raise
from io import StringIO
from typing import ContextManager, Optional, Tuple, Type

import pytest
from pytest_mock import MockerFixture
from rich.console import Console, RenderableType
from rich.live import Live
from rich.spinner import Spinner
from zeroconf import ServiceStateChange

from mdns_beacon.cli.layouts import BaseLayout, BlinkLayout, ListenLayout


def render(renderable: RenderableType) -> str:
    """Get the string representation of a renderable object."""
    console = Console(
        width=60,
        force_terminal=True,
        file=StringIO(),
        legacy_windows=False,
        color_system=None,
    )

    console.print(renderable)

    return console.file.getvalue()  # type: ignore


class DummyLayout(BaseLayout):
    """Dummy Layout for purpose."""

    spinner_text = "Dummy spinner ..."

    @property
    def renderable(self) -> Spinner:
        """Render dummy spinner."""
        return self.spinner


@pytest.mark.parametrize(
    "layout_class,expected",
    [
        (DummyLayout, DummyLayout.spinner_text),
        (BlinkLayout, BlinkLayout.spinner_text),
        (ListenLayout, ListenLayout.spinner_text),
    ],
)
def test_render_layout(layout_class: Type[BaseLayout], expected: str) -> None:
    """Test render layout."""
    with Live("") as live:
        layout = layout_class(live=live)

        assert expected in render(layout.renderable)

    assert not live._started


@pytest.mark.parametrize(
    "show_columns,raises,state_change",
    [
        (None, does_not_raise(), ServiceStateChange.Removed),
        (tuple(), does_not_raise(), ServiceStateChange.Removed),
        (("weight", "priority", "text", "properties"), does_not_raise(), ServiceStateChange.Added),
        (
            ("weight", "priority", "text", "wrong_column"),
            pytest.raises(ValueError),
            ServiceStateChange.Added,
        ),
    ],
)
def test_listen_layout(
    mocker: MockerFixture,
    show_columns: Optional[Tuple[str]],
    raises: ContextManager,
    state_change: ServiceStateChange,
) -> None:
    """Text listen layout."""
    zeroconf = mocker.MagicMock()
    zeroconf.get_service_info = mocker.MagicMock(return_value=None)  # Never returns a service info

    with Live("") as live, raises:
        layout = ListenLayout(live=live, show_columns=show_columns)
        assert layout.services == {}
        layout.update_services(
            zeroconf=zeroconf,
            service_type="._some._type.local.",
            name="some_name",
            state_change=state_change,
        )
        assert layout.services == {}

    assert not live._started
