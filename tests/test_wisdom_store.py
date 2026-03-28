"""Quotes store against a temp JSON file."""

import json
from pathlib import Path

from wise_yoda.wisdom import Quotes


def test_select_exact(tmp_path: Path, quote_data: dict) -> None:
    p = tmp_path / "q.json"
    p.write_text(json.dumps(quote_data), encoding="utf-8")
    store = Quotes(p)
    q = store.select_quote(2, 1)
    assert q is not None
    assert q.title == "Rising Malevolence"


def test_search_hits(tmp_path: Path, quote_data: dict) -> None:
    p = tmp_path / "q.json"
    p.write_text(json.dumps(quote_data), encoding="utf-8")
    store = Quotes(p)
    hits = store.search("fear")
    assert len(hits) == 1
    assert "Fear" in hits[0].description


def test_random_is_stable_pool(tmp_path: Path, quote_data: dict) -> None:
    p = tmp_path / "q.json"
    p.write_text(json.dumps(quote_data), encoding="utf-8")
    store = Quotes(p)
    q = store.random_quote()
    assert q in store.quotes
