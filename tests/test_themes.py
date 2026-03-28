"""Theme resolution."""

from wise_yoda.themes import resolve_theme


def test_unknown_theme_falls_back() -> None:
    t = resolve_theme("not-a-real-theme")
    assert t.panel_border == "green"
