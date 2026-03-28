"""Quote-seeded terminal ASCII intros (Rich Live, TTY only)."""

from __future__ import annotations

import hashlib
import random
import time
from collections.abc import Callable

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from .wisdom import Quote

FrameBuilder = Callable[[random.Random], list[str]]


def quote_seed(q: Quote) -> int:
    """Stable seed so the same lesson always gets the same animation family."""
    raw = f"{q.season}:{q.episode}:{q.title}:{q.description}".encode()
    return int(hashlib.blake2b(raw, digest_size=4).hexdigest(), 16)


def _saber_frames(rng: random.Random) -> list[str]:
    """Pulsing column blade + hilt (ASCII + Rich color)."""
    hue = rng.choice(["green", "yellow", "cyan", "magenta"])
    frames: list[str] = []
    for phase in range(14):
        h = 2 + (phase % 6)
        lines = ["       ^", "       |"]
        for _ in range(h):
            lines.append(f"       [bold {hue}]|[/bold {hue}]")
        lines.append(f"     [bold {hue}]--+--O[/bold {hue}]")
        lines.append("   [dim] ~ the Force ~ [/dim]")
        frames.append("\n".join(lines))
    return frames


def _starfield_frames(rng: random.Random) -> list[str]:
    """Tiny sky; twinkle from rng."""
    w, h = 38, 9
    chars = ".*+x"
    frames: list[str] = []
    for _ in range(16):
        grid = [[" " for _ in range(w)] for _ in range(h)]
        k = rng.randint(20, 48)
        for _ in range(k):
            grid[rng.randint(0, h - 1)][rng.randint(0, w - 1)] = rng.choice(chars)
        row = h // 2 + 1
        for x in range(w):
            if grid[row][x] == " " and rng.random() < 0.12:
                grid[row][x] = "-"
        lines = ["".join(r) for r in grid]
        frames.append("\n".join(lines))
    return frames


def _yoda_frames(rng: random.Random) -> list[str]:
    """Tiny sage; eyes blink."""
    blink = rng.choice([True, False])
    frames: list[str] = []
    for i in range(10):
        eyes = "o o" if (i % 3 != 1) ^ blink else "- -"
        ear_l = "/" if i % 2 == 0 else ","
        ear_r = "\\" if i % 2 == 0 else ","
        art = f"""[dim]
          .-----.
         {ear_l}       {ear_r}
        |   {eyes}   |
        |    v    |
         \\  ---  /
          `-----'
[/dim][green]   ~ listen, you must ~[/green]"""
        frames.append(art)
    return frames


def _swirl_frames(rng: random.Random) -> list[str]:
    """Orbiting punctuation (quote energy)."""
    frames: list[str] = []
    for t in range(20):
        a = (t * 2) % 6
        b = 6 - a
        ring = f"{'~' * a} * {'~' * b}"
        inner = rng.choice(["+", "x", "*", "o"])
        frames.append(
            f"\n{' ' * 8}{ring}\n{' ' * 12}[bold cyan]{inner}[/bold cyan]\n{' ' * 8}{ring[::-1]}\n"
        )
    return frames


_PRESETS: list[FrameBuilder] = [_saber_frames, _starfield_frames, _yoda_frames, _swirl_frames]


def build_frames(quote: Quote) -> list[str]:
    rng = random.Random(quote_seed(quote))  # noqa: S311  # visual variety only
    builder = rng.choice(_PRESETS)
    return builder(rng)


def play_intro(
    quote: Quote,
    console: Console,
    *,
    border_style: str,
    seconds: float = 2.75,
    refresh_per_second: float = 14.0,
) -> None:
    """Play looping frames for ``seconds`` (no-op if not a TTY)."""
    if not console.is_terminal:
        return
    frames = build_frames(quote)
    if not frames:
        return
    sleep = 1.0 / refresh_per_second
    deadline = time.monotonic() + max(0.4, seconds)
    idx = 0
    with Live(
        console=console,
        refresh_per_second=refresh_per_second,
        transient=True,
    ) as live:
        while time.monotonic() < deadline:
            body = frames[idx % len(frames)]
            panel = Panel(
                Align.center(Text.from_markup(body, justify="center")),
                title="[dim italic]the Force gathers…[/dim italic]",
                border_style=border_style,
                padding=(0, 1),
            )
            live.update(panel)
            idx += 1
            time.sleep(sleep)
