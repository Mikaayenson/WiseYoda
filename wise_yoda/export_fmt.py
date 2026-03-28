"""Markdown and CSV serializers for lesson lists."""

from __future__ import annotations

import csv
import io

from .wisdom import Quote


def quotes_to_markdown(quotes: list[Quote]) -> str:
    lines: list[str] = ["# WiseYoda export", ""]
    for q in quotes:
        lines.append(f"## S{q.season:02d}E{q.episode:02d} — {q.title}")
        lines.append("")
        lines.append(q.description)
        lines.append("")
    return "\n".join(lines)


def quotes_to_csv(quotes: list[Quote]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["season", "episode", "title", "description"])
    for q in quotes:
        writer.writerow([q.season, q.episode, q.title, q.description])
    return buf.getvalue()
