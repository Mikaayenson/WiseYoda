"""Terminal color presets (CLI --theme or WISEYODA_THEME)."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """Rich styles for panels and tables."""

    panel_title: str
    panel_border: str
    table_title: str
    table_header: str
    table_border: str
    archive_border: str


_PRESETS: dict[str, Theme] = {
    "green": Theme(
        panel_title="bold green",
        panel_border="green",
        table_title="green",
        table_header="bold green",
        table_border="green",
        archive_border="green",
    ),
    "blue": Theme(
        panel_title="bold blue",
        panel_border="blue",
        table_title="blue",
        table_header="bold blue",
        table_border="blue",
        archive_border="blue",
    ),
    "magenta": Theme(
        panel_title="bold magenta",
        panel_border="magenta",
        table_title="magenta",
        table_header="bold magenta",
        table_border="magenta",
        archive_border="magenta",
    ),
    "gold": Theme(
        panel_title="bold yellow",
        panel_border="yellow",
        table_title="yellow",
        table_header="bold yellow",
        table_border="yellow",
        archive_border="yellow",
    ),
    "dim": Theme(
        panel_title="bold white",
        panel_border="dim",
        table_title="dim",
        table_header="bold white",
        table_border="dim",
        archive_border="dim",
    ),
}


def resolve_theme(name: str | None) -> Theme:
    """Resolve --theme or WISEYODA_THEME; unknown names fall back to green."""
    key = (name or os.environ.get("WISEYODA_THEME") or "green").strip().casefold()
    return _PRESETS.get(key, _PRESETS["green"])
