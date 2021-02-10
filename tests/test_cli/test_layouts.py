"""Tests for `mdns_beacon.cli.layouts` module."""
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from mdns_beacon.cli.layouts import BaseLayout


class DummyLayout(BaseLayout):
    """Dummy Layout for purpose."""

    spinner_text = "Dummy spinner ..."

    @property
    def renderable(self) -> Spinner:
        """Render dummy spinner."""
        return self.spinner


def test_base_layout() -> None:
    """Test base layout."""
    with Live("") as live:
        layout = DummyLayout(live=live)
        assert layout.renderable.text == Text("Dummy spinner ...")

    assert not live._started
