"""WISEYODA_QUOTES and resolve_quotes_path."""

import json
from pathlib import Path

import pytest
from wise_yoda.wisdom import Quotes, resolve_quotes_path


def test_resolve_explicit_path(tmp_path: Path, quote_data: dict) -> None:
    p = tmp_path / "q.json"
    p.write_text(json.dumps(quote_data), encoding="utf-8")
    assert resolve_quotes_path(p) == p.resolve()


def test_resolve_from_env(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    quote_data: dict,
) -> None:
    p = tmp_path / "env.json"
    p.write_text(json.dumps(quote_data), encoding="utf-8")
    monkeypatch.setenv("WISEYODA_QUOTES", str(p))
    assert resolve_quotes_path(None) == p.resolve()
    store = Quotes()
    assert store.count() == 2
