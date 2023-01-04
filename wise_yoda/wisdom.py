"""Wisdom module."""
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path

from marshmallow_dataclass import class_schema

QUOTES_DB = Path(__file__).parent / "data" / "quotes.json"


@dataclass
class QuoteSchema:
    """Quote schema."""

    season: int
    episode: int
    title: str
    description: str

    def __iter__(self):
        """Iterator to return a dict of the quote."""
        for key in asdict(self):
            yield key, getattr(self, key)

    def __str__(self) -> str:
        """Return a pretty quote."""
        return f"{self.season}x{self.episode} - {self.title}\n{self.description}"


@dataclass
class QuoteList:
    """List of QuoteSchema."""

    data: list[QuoteSchema]


class Quotes:
    """Load quotes from a json db file."""

    def __init__(self, filename: Path = QUOTES_DB):
        """Initialize the Quotes class."""
        self.filename = filename
        self.quotes = self.load()

    def load(self) -> QuoteList:
        """Load quotes from a json file."""
        with open(self.filename, encoding="utf-8") as file:
            data = json.load(file)
            schema = class_schema(QuoteList)()
            return schema.load(data)

    def dump(self, quotes: QuoteList, filename: Path = None) -> None:
        """Dump quotes to a json file."""
        if not filename:
            filename = self.filename

        schema = class_schema(QuoteList)()
        data = schema.dump(quotes)
        with open(filename, "w", encoding="utf-8") as quotes_file:
            json.dump(data, quotes_file, indent=4)

    def select_quote(self, season: int, episode: int) -> QuoteSchema:
        """Return a quote from a specific season and episode."""
        if season and episode:
            quote = next(
                (quote for quote in self.quotes.data if quote.season == season and quote.episode == episode),
                None,
            )
        elif season:
            quote = next(
                (quote for quote in self.quotes.data if quote.season == season),
                None,
            )
        elif episode:
            quote = next(
                (quote for quote in self.quotes.data if quote.episode == episode),
                None,
            )
        return quote

    def random_quote(self) -> QuoteSchema:
        """Return a random quote."""
        quote = random.choice(self.quotes.data)  # nosec
        return quote


QUOTESCHEMA = class_schema(QuoteSchema)()
QUOTELISTSCHEMA = class_schema(QuoteList)()
