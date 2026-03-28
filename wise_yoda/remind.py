"""Shell one-liners for desktop notifications (macOS / Linux)."""

from __future__ import annotations

import shlex

from .wisdom import Quote
from .yoda_style import to_yoda_speak


def reminder_script(quote: Quote, *, yoda: bool) -> str:
    """Return commented copy-paste commands for notify-send and osascript."""
    body = to_yoda_speak(quote.description) if yoda else quote.description
    one = " ".join(body.split())[:400]
    title = f"S{quote.season:02d}E{quote.episode:02d} · {quote.title}"
    title_short = title[:120]

    def dq_esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    script = f'display notification "{dq_esc(one)}" with title "{dq_esc(title_short)}"'
    osa = f"osascript -e {shlex.quote(script)}"
    linux = f"notify-send {shlex.quote(title_short)} {shlex.quote(one)}"

    return (
        f"# WiseYoda — pick ONE line for your OS\n# macOS:\n{osa}\n# Linux (libnotify):\n{linux}\n"
    )
