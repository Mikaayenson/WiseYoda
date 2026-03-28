"""Quote-seeded ASCII animation helpers."""

import io

from rich.console import Console
from wise_yoda.ascii_anim import build_frames, play_intro, quote_seed
from wise_yoda.wisdom import Quote


def test_quote_seed_stable() -> None:
    q = Quote(season=1, episode=2, title="T", description="hello")
    assert quote_seed(q) == quote_seed(q)


def test_quote_seed_differs_when_text_differs() -> None:
    a = Quote(season=1, episode=1, title="T", description="a")
    b = Quote(season=1, episode=1, title="T", description="b")
    assert quote_seed(a) != quote_seed(b)


def test_build_frames_non_empty() -> None:
    q = Quote(season=3, episode=5, title="X", description="y")
    frames = build_frames(q)
    assert frames
    assert all(isinstance(f, str) and f.strip() for f in frames)


def test_play_intro_no_tty_no_crash() -> None:
    q = Quote(season=1, episode=1, title="T", description="d")
    c = Console(file=io.StringIO(), force_terminal=False)
    play_intro(q, c, border_style="green", seconds=0.1)
