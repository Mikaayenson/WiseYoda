#

<div align="center">
  <img width="500" alt="logo" src="https://user-images.githubusercontent.com/1636709/210475936-9943ee5d-6bec-488d-a309-7a0df2312291.png">
  <h1>WiseYoda</h1>

  <p>
    Quotes from the <a href="https://github.com/Mikaayenson/WiseYoda">Wise Yoda</a>
  </p>

[![Supported Python versions](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Python Testing](https://github.com/Mikaayenson/WiseYoda/actions/workflows/python-testing.yml/badge.svg)](https://github.com/Mikaayenson/WiseYoda/actions/workflows/python-testing.yml)

<h5>
    <a href="https://github.com/Mikaayenson/WiseYoda/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Mikaayenson/WiseYoda/issues/">Request Feature</a>
  </h5>
</div>

<br />

## About

**WiseYoda** is a small **library** and **terminal app** for browsing bundled “opening crawl”–style lessons (season, episode, title, description). The CLI uses [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/); with **`--animate`**, you get a **quote-seeded moving ASCII intro** (lightsaber pulse, starfield, little sage, or swirl) before the wisdom panel. Data is validated with [Pydantic v2](https://docs.pydantic.dev/). An optional **FastAPI** layer serves JSON for scripts and dashboards (`wiseyoda[api]`).

Stack: **Python 3.11+**, **[uv](https://docs.astral.sh/uv/)**, **[Ruff](https://docs.astral.sh/ruff/)**, **pytest** + coverage in CI.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `WISEYODA_QUOTES` | Path to a `quotes.json` file (default database when `-f` is omitted). |
| `WISEYODA_THEME` | Default panel/table theme: `green`, `blue`, `magenta`, `gold`, `dim`. |

## Install

```bash
uv tool install wiseyoda
# optional HTTP server:
uv tool install "wiseyoda[api]"
# or: pip install wiseyoda
```

## CLI quick reference

| Command | What it does |
|--------|----------------|
| `wiseyoda` | Random lesson (Rich panel) |
| `wiseyoda -s 1 -e 3` | Lesson for season 1, episode 3 |
| `wiseyoda -1` / `--oneline` | One line (description only) — e.g. `wiseyoda -1 \| cowsay` |
| `wiseyoda --yoda` | Toy “Yoda shuffle” on the text |
| `wiseyoda --theme blue` | Panel/table colors (or set `WISEYODA_THEME`) |
| `wiseyoda --animate` | **Moving ASCII intro** (seeded by the quote), then the wisdom panel |
| `wiseyoda --animate --animate-seconds 4` | Longer intro (0.5–30s) |
| `wiseyoda -j` | JSON on stdout (safe for piping; no Rich markup) |
| `wiseyoda random` | Explicit random |
| `wiseyoda search fear` | Keyword search (table) |
| `wiseyoda list --limit 20` | Tabular listing |
| `wiseyoda stats` | Totals per season |
| `wiseyoda pipe` | Read one Quote JSON from **stdin**; write text or JSON to stdout |
| `wiseyoda export markdown` | Full archive as Markdown (stdout) |
| `wiseyoda export csv` | Full archive as CSV (stdout) |
| `wiseyoda export md -s 1` | Same, one season only |
| `wiseyoda remind -r` | Print **osascript** / **notify-send** one-liners for a notification |
| `wiseyoda serve --port 8765` | Local JSON API (needs `pip install 'wiseyoda[api]'`) |
| `wiseyoda version` | Package version |

Use `-f path/to/quotes.json` to override the file for one invocation (still respects Typer’s “file must exist” check).

### Shell tab completion

Typer adds completion flags to the program itself:

```bash
wiseyoda --install-completion
# or: wiseyoda --show-completion
```

Follow the printed instructions for your shell (bash, zsh, fish, PowerShell).

### HTTP API (with `wiseyoda[api]`)

After `wiseyoda serve` (default `http://127.0.0.1:8765`):

- `GET /health` — `{ "status": "ok" }`
- `GET /random` — one quote object
- `GET /quote?season=1&episode=1` — lookup (or omit both for random)
- `GET /search?q=wisdom&limit=50` — JSON array
- `GET /stats` — totals and counts per season

## Library

```python
from wise_yoda import Quotes, resolve_quotes_path

# Uses bundled JSON unless WISEYODA_QUOTES is set or you pass a path:
store = Quotes()
lesson = store.random_quote()
lesson = store.select_quote(season=1, episode=1)
for hit in store.search("wisdom"):
    print(hit.description)
```

## Develop locally

```bash
git clone https://github.com/Mikaayenson/WiseYoda.git
cd WiseYoda
make sync    # uv sync --extra dev --extra api
make check   # ruff
make test    # pytest + coverage
make build   # wheel + sdist
```

Optional: `pre-commit install`.

## License

Apache-2.0. See [LICENSE](LICENSE).
