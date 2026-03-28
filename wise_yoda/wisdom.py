"""Load and query Yoda wisdom from bundled JSON."""

from __future__ import annotations

import json
import os
import random
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

QUOTES_DB = Path(__file__).resolve().parent / "data" / "quotes.json"


def resolve_quotes_path(filename: Path | None) -> Path:
    """`-f` wins; else ``WISEYODA_QUOTES``; else bundled ``quotes.json``."""
    if filename is not None:
        return Path(filename).expanduser().resolve()
    env = os.environ.get("WISEYODA_QUOTES", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return QUOTES_DB


class Quote(BaseModel):
    """A single opening-crawl style lesson tied to an episode."""

    model_config = ConfigDict(frozen=True)

    season: int = Field(ge=1)
    episode: int = Field(ge=1)
    title: str
    description: str

    def format_plain(self) -> str:
        return f"{self.season}x{self.episode} - {self.title}\n{self.description}"


class QuoteBundle(BaseModel):
    """Top-level shape of quotes.json."""

    data: list[Quote]


class Quotes:
    """Load quotes from a JSON file (defaults to the bundled database)."""

    def __init__(self, filename: Path | None = None) -> None:
        self.filename = resolve_quotes_path(filename)
        self._bundle = self._load()

    def _load(self) -> QuoteBundle:
        with self.filename.open(encoding="utf-8") as f:
            raw = json.load(f)
        return QuoteBundle.model_validate(raw)

    @property
    def quotes(self) -> list[Quote]:
        return self._bundle.data

    def reload(self) -> None:
        """Reread the file from disk (useful after edits)."""
        self._bundle = self._load()

    def save(self, path: Path | None = None) -> None:
        """Write the current bundle to JSON (handy for tooling)."""
        out = path or self.filename
        payload = self._bundle.model_dump(mode="json")
        with Path(out).open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
            f.write("\n")

    def select_quote(self, season: int | None, episode: int | None) -> Quote | None:
        """First quote matching season and/or episode filters."""
        if season is not None and episode is not None:
            return next(
                (q for q in self.quotes if q.season == season and q.episode == episode),
                None,
            )
        if season is not None:
            return next((q for q in self.quotes if q.season == season), None)
        if episode is not None:
            return next((q for q in self.quotes if q.episode == episode), None)
        return None

    def random_quote(self) -> Quote:
        return random.choice(self.quotes)  # noqa: S311  # cryptographically fine for quotes

    def search(self, query: str, *, limit: int = 50) -> list[Quote]:
        """Case-insensitive match on title or description."""
        q = query.casefold().strip()
        if not q:
            return []
        hits: list[Quote] = []
        for item in self.quotes:
            if q in item.title.casefold() or q in item.description.casefold():
                hits.append(item)
                if len(hits) >= limit:
                    break
        return hits

    def count(self) -> int:
        return len(self.quotes)

    def seasons(self) -> list[int]:
        seen: set[int] = set()
        ordered: list[int] = []
        for q in self.quotes:
            if q.season not in seen:
                seen.add(q.season)
                ordered.append(q.season)
        return ordered
