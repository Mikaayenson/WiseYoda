"""Pydantic models load and dump like the legacy schema tests."""

import json

from wise_yoda.wisdom import Quote, QuoteBundle


def test_quote_from_dict(quote_data: dict) -> None:
    raw = quote_data["data"][0]
    q = Quote.model_validate(raw)
    assert q.title == "Ambush"
    assert q.description == "Great leaders inspire greatness in others."
    assert q.season == 1
    assert q.episode == 1


def test_quote_roundtrip_json(quote_data: dict) -> None:
    raw = quote_data["data"][0]
    q = Quote.model_validate(raw)
    dumped = q.model_dump()
    assert dumped == raw


def test_bundle_loads(quote_data: dict) -> None:
    bundle = QuoteBundle.model_validate(quote_data)
    assert len(bundle.data) == 2
    assert bundle.data[0].title == "Ambush"
    assert bundle.data[1].title == "Rising Malevolence"
    assert bundle.data[1].season == 2
    assert bundle.data[1].episode == 1


def test_bundle_json_roundtrip(quote_data: dict) -> None:
    bundle = QuoteBundle.model_validate(quote_data)
    s = json.dumps(bundle.model_dump())
    again = QuoteBundle.model_validate_json(s)
    assert again.model_dump() == bundle.model_dump()


def test_quote_format_plain(quote_data: dict) -> None:
    q = Quote.model_validate(quote_data["data"][0])
    text = q.format_plain()
    assert "Ambush" in text
    assert "Great leaders" in text
