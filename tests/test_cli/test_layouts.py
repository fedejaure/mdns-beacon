"""Tests for `mdns_beacon.cli.layouts` module."""
from io import StringIO
from typing import Type

import pytest
from rich.console import Console, RenderableType
from rich.live import Live
from rich.spinner import Spinner

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
