"""Tiny JSON HTTP API (optional: pip install 'wiseyoda[api]')."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from .wisdom import QUOTES_DB, Quotes


def _pkg_version() -> str:
    try:
        return version("wiseyoda")
    except PackageNotFoundError:
        return "0.0.0-dev"


def build_app(*, quotes_path: Path | None = None) -> FastAPI:
    path = quotes_path or QUOTES_DB
    store = Quotes(path)

    app = FastAPI(
        title="WiseYoda",
        description="Random and lookup JSON API over the lesson database.",
        version=_pkg_version(),
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/random")
    def random_quote() -> dict:
        return store.random_quote().model_dump()

    @app.get("/quote", response_model=None)
    def one_quote(
        season: int | None = Query(None, ge=1),
        episode: int | None = Query(None, ge=1),
    ) -> dict:
        if season is None and episode is None:
            return store.random_quote().model_dump()
        q = store.select_quote(season, episode)
        if q is None:
            raise HTTPException(status_code=404, detail="No quote for those filters.")
        return q.model_dump()

    @app.get("/search")
    def search(
        q: str = Query(..., min_length=1),
        limit: int = Query(50, ge=1, le=500),
    ) -> list[dict]:
        hits = store.search(q, limit=limit)
        return [h.model_dump() for h in hits]

    @app.get("/stats")
    def stats() -> dict:
        by_season: dict[int, int] = {}
        for quote in store.quotes:
            by_season[quote.season] = by_season.get(quote.season, 0) + 1
        pairs = sorted(by_season.items())
        return {"total": store.count(), "by_season": {str(k): v for k, v in pairs}}

    return app
