"""Argparse configuration for wise_yoda."""
import argparse
import json
from pathlib import Path

from .wisdom import Quotes


def main():
    """Parse arguments and run the program."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--filename", help="File to read quotes from", default=Path().cwd() / "data" / "quotes.json"
    )

    # add option to select quote by season, episode, or random
    parser.add_argument(
        "-s",
        "--season",
        help="Select a quote by season",
        type=int,
        default=None,
    )
    parser.add_argument(
        "-e",
        "--episode",
        help="Select a quote by episode",
        type=int,
        default=None,
    )
    parser.add_argument(
        "-r",
        "--random",
        help="Select a random quote",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-j",
        "--json",
        help="Output quote as json",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    # Demo of the Quote class
    if args.random or (not args.season and not args.episode):
        quote = Quotes().random_quote()
    else:
        quote = Quotes().select_quote(args.season, args.episode)

    if args.json:
        print(json.dumps(dict(quote), indent=2))
    else:
        print(quote)


if __name__ == "__main__":
    main()
