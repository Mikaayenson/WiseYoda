"""Typer CLI: wisdom from the bundled Clone Wars–style lesson file."""

from __future__ import annotations

import json
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .ascii_anim import play_intro
from .export_fmt import quotes_to_csv, quotes_to_markdown
from .remind import reminder_script
from .themes import Theme, resolve_theme
from .wisdom import Quote, Quotes, resolve_quotes_path
from .yoda_style import to_yoda_speak

FilenameOpt = Annotated[
    Path | None,
    typer.Option(
        "-f",
        "--filename",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Quotes JSON (default: bundled DB or WISEYODA_QUOTES).",
    ),
]

ThemeOpt = Annotated[
    str | None,
    typer.Option(
        "--theme",
        help="Panel/table colors: green, blue, magenta, gold, dim (or WISEYODA_THEME).",
    ),
]

app = typer.Typer(
    name="wiseyoda",
    help="Wisdom from Master Yoda — ASCII intros, search, API, exports.",
    rich_markup_mode="rich",
    no_args_is_help=False,
    add_completion=True,
)
console = Console()


def _pkg_version() -> str:
    try:
        return version("wiseyoda")
    except PackageNotFoundError:
        return "0.0.0-dev"


def _maybe_play_intro(
    quote: Quote,
    theme: Theme,
    *,
    animate: bool,
    animate_seconds: float,
    as_json: bool,
    plain: bool,
    oneline: bool,
) -> None:
    if not animate:
        return
    if as_json or plain or oneline:
        console.print(
            "[dim]--animate ignored with -j, --plain, or -1[/dim]",
            file=sys.stderr,
        )
        return
    if not console.is_terminal:
        console.print(
            "[dim]--animate needs an interactive terminal[/dim]",
            file=sys.stderr,
        )
        return
    play_intro(
        quote,
        console,
        border_style=theme.panel_border,
        seconds=animate_seconds,
    )


def _render_quote(
    quote: Quote,
    theme: Theme,
    *,
    as_json: bool,
    yoda: bool,
    plain: bool,
    oneline: bool,
) -> None:
    body = to_yoda_speak(quote.description) if yoda else quote.description
    if as_json:
        data = quote.model_dump()
        if yoda:
            data["description_yoda"] = to_yoda_speak(quote.description)
        sep = (",", ":") if oneline else None
        ind = None if oneline else 2
        sys.stdout.write(json.dumps(data, separators=sep, indent=ind) + "\n")
        return
    if oneline:
        line = " ".join(body.split())
        console.print(line)
        return
    if plain:
        if yoda:
            hdr = f"{quote.season}x{quote.episode} - {quote.title}"
            console.print(f"{hdr}\n{body}")
        else:
            console.print(quote.format_plain())
        return
    subtitle = f"[dim]{quote.title} · S{quote.season:02d}E{quote.episode:02d}[/dim]"
    panel = Panel(
        f"[italic]{body}[/italic]\n\n{subtitle}",
        title=f"[{theme.panel_title}]Master Yoda[/{theme.panel_title}]",
        border_style=theme.panel_border,
        padding=(1, 2),
    )
    console.print(panel)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    filename: FilenameOpt = None,
    season: Annotated[
        int | None,
        typer.Option("-s", "--season", help="Filter by season."),
    ] = None,
    episode: Annotated[
        int | None,
        typer.Option("-e", "--episode", help="Filter by episode."),
    ] = None,
    random: Annotated[
        bool,
        typer.Option("-r", "--random", help="Pick a random quote (overrides filters)."),
    ] = False,
    as_json: Annotated[
        bool,
        typer.Option("-j", "--json", help="Emit JSON instead of a Rich panel."),
    ] = False,
    yoda: Annotated[
        bool,
        typer.Option("--yoda", help="Toy clause shuffle for a Yoda-style line."),
    ] = False,
    plain: Annotated[
        bool,
        typer.Option("--plain", help="Plain text (no panel)."),
    ] = False,
    oneline: Annotated[
        bool,
        typer.Option(
            "-1",
            "--oneline",
            help="Single line (description only) — handy for fortune | cowsay.",
        ),
    ] = False,
    theme_name: ThemeOpt = None,
    animate: Annotated[
        bool,
        typer.Option(
            "--animate",
            help="Quote-seeded moving ASCII intro, then the panel (TTY only).",
        ),
    ] = False,
    animate_seconds: Annotated[
        float,
        typer.Option(
            "--animate-seconds",
            min=0.5,
            max=30.0,
            help="Length of the ASCII intro.",
        ),
    ] = 2.75,
) -> None:
    """With no subcommand: show one quote (random unless --season / --episode narrow it)."""
    if ctx.invoked_subcommand is not None:
        return
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    theme = resolve_theme(theme_name)
    if random:
        q = store.random_quote()
    elif season is not None or episode is not None:
        q = store.select_quote(season, episode)
        if q is None:
            console.print("[red]No quote matched those filters.[/red]", file=sys.stderr)
            raise typer.Exit(code=1)
    else:
        q = store.random_quote()
    _maybe_play_intro(
        q,
        theme,
        animate=animate,
        animate_seconds=animate_seconds,
        as_json=as_json,
        plain=plain,
        oneline=oneline,
    )
    _render_quote(q, theme, as_json=as_json, yoda=yoda, plain=plain, oneline=oneline)


@app.command("random")
def cmd_random(
    filename: FilenameOpt = None,
    as_json: Annotated[bool, typer.Option("-j", "--json")] = False,
    yoda: Annotated[bool, typer.Option("--yoda")] = False,
    plain: Annotated[bool, typer.Option("--plain")] = False,
    oneline: Annotated[bool, typer.Option("-1", "--oneline")] = False,
    theme_name: ThemeOpt = None,
    animate: Annotated[
        bool,
        typer.Option("--animate", help="Quote-seeded ASCII intro before the panel."),
    ] = False,
    animate_seconds: Annotated[
        float,
        typer.Option("--animate-seconds", min=0.5, max=30.0),
    ] = 2.75,
) -> None:
    """Random lesson from the database."""
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    theme = resolve_theme(theme_name)
    q = store.random_quote()
    _maybe_play_intro(
        q,
        theme,
        animate=animate,
        animate_seconds=animate_seconds,
        as_json=as_json,
        plain=plain,
        oneline=oneline,
    )
    _render_quote(
        q,
        theme,
        as_json=as_json,
        yoda=yoda,
        plain=plain,
        oneline=oneline,
    )


@app.command("search")
def cmd_search(
    query: Annotated[str, typer.Argument(help="Substring to find in title or description.")],
    filename: FilenameOpt = None,
    limit: Annotated[int, typer.Option("--limit", min=1, max=500, help="Max rows.")] = 30,
    as_json: Annotated[bool, typer.Option("-j", "--json")] = False,
    theme_name: ThemeOpt = None,
) -> None:
    """Search lessons by keyword."""
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    theme = resolve_theme(theme_name)
    hits = store.search(query, limit=limit)
    if not hits:
        console.print("[yellow]No matches.[/yellow]")
        raise typer.Exit(code=0)
    if as_json:
        sys.stdout.write(json.dumps([h.model_dump() for h in hits], indent=2) + "\n")
        return
    table = Table(
        title=f"Matches for “{query}”",
        show_lines=False,
        border_style=theme.table_border,
        header_style=theme.table_header,
        title_style=theme.table_title,
    )
    table.add_column("S", justify="right", style="cyan", no_wrap=True)
    table.add_column("E", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Lesson", overflow="ellipsis", max_width=56)
    for h in hits:
        table.add_row(str(h.season), str(h.episode), h.title, h.description)
    console.print(table)


@app.command("list")
def cmd_list(
    filename: FilenameOpt = None,
    season: Annotated[int | None, typer.Option("-s", "--season", help="Only this season.")] = None,
    limit: Annotated[int, typer.Option("--limit", min=1, max=2000, help="Max rows.")] = 80,
    theme_name: ThemeOpt = None,
) -> None:
    """Tabular listing (trimmed by --limit)."""
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    theme = resolve_theme(theme_name)
    rows = [q for q in store.quotes if season is None or q.season == season][:limit]
    table = Table(
        title="Lessons",
        show_header=True,
        border_style=theme.table_border,
        header_style=theme.table_header,
        title_style=theme.table_title,
    )
    table.add_column("S", justify="right")
    table.add_column("E", justify="right")
    table.add_column("Title", style="bold")
    table.add_column("Opening line", overflow="ellipsis", max_width=50)
    for q in rows:
        first = q.description.split("\n")[0][:80]
        table.add_row(str(q.season), str(q.episode), q.title, first)
    console.print(table)
    if len(rows) < store.count():
        msg = f"[dim]Showing {len(rows)} of {store.count()}; use --limit for more.[/dim]"
        console.print(msg)


@app.command("stats")
def cmd_stats(
    filename: FilenameOpt = None,
    theme_name: ThemeOpt = None,
) -> None:
    """Counts and season overview."""
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    theme = resolve_theme(theme_name)
    by_season: dict[int, int] = {}
    for q in store.quotes:
        by_season[q.season] = by_season.get(q.season, 0) + 1
    total = store.count()
    archive = Panel.fit(
        f"[bold]Total lessons:[/bold] {total}",
        title="Archive",
        border_style=theme.archive_border,
    )
    console.print(archive)
    t = Table(
        title="Per season",
        border_style=theme.table_border,
        header_style=theme.table_header,
        title_style=theme.table_title,
    )
    t.add_column("Season", justify="right")
    t.add_column("Lessons", justify="right")
    for s in sorted(by_season):
        t.add_row(str(s), str(by_season[s]))
    console.print(t)


@app.command("pipe")
def cmd_pipe(
    yoda: Annotated[
        bool,
        typer.Option("--yoda", help="Toy Yoda shuffle on description."),
    ] = False,
    as_json: Annotated[
        bool,
        typer.Option("-j", "--json", help="Write JSON to stdout."),
    ] = False,
) -> None:
    """Read one Quote JSON object from stdin; write text or JSON to stdout (for scripts)."""
    raw = sys.stdin.read()
    if not raw.strip():
        msg = "[red]stdin was empty; expected JSON: season, episode, title, description.[/red]"
        console.print(msg, file=sys.stderr)
        raise typer.Exit(code=1)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON: {e}[/red]", file=sys.stderr)
        raise typer.Exit(code=1) from e
    try:
        q = Quote.model_validate(data)
    except Exception as e:
        console.print(f"[red]Not a valid quote object: {e}[/red]", file=sys.stderr)
        raise typer.Exit(code=1) from e
    body = to_yoda_speak(q.description) if yoda else q.description
    if as_json:
        out = q.model_dump()
        if yoda:
            out["description_yoda"] = body
        sys.stdout.write(json.dumps(out, indent=2) + "\n")
        return
    sys.stdout.write(body + "\n")


@app.command("export")
def cmd_export(
    fmt: Annotated[str, typer.Argument(help="markdown | csv")],
    filename: FilenameOpt = None,
    season: Annotated[int | None, typer.Option("-s", "--season", help="Only this season.")] = None,
) -> None:
    """Dump the archive as Markdown or CSV (stdout)."""
    key = fmt.strip().casefold()
    if key not in {"markdown", "md", "csv"}:
        console.print("[red]Format must be markdown (or md) or csv.[/red]", file=sys.stderr)
        raise typer.Exit(code=1)
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    rows = [q for q in store.quotes if season is None or q.season == season]
    if key == "csv":
        sys.stdout.write(quotes_to_csv(rows))
    else:
        sys.stdout.write(quotes_to_markdown(rows))


@app.command("remind")
def cmd_remind(
    filename: FilenameOpt = None,
    season: Annotated[int | None, typer.Option("-s", "--season")] = None,
    episode: Annotated[int | None, typer.Option("-e", "--episode")] = None,
    random_pick: Annotated[
        bool,
        typer.Option("-r", "--random", help="Random lesson (default if no season/episode)."),
    ] = False,
    yoda: Annotated[bool, typer.Option("--yoda")] = False,
) -> None:
    """Print copy-paste osascript / notify-send lines for desktop notification."""
    path = resolve_quotes_path(filename)
    store = Quotes(path)
    if random_pick or (season is None and episode is None):
        q = store.random_quote()
    else:
        q = store.select_quote(season, episode)
        if q is None:
            console.print("[red]No quote matched those filters.[/red]", file=sys.stderr)
            raise typer.Exit(code=1)
    console.print(reminder_script(q, yoda=yoda), end="")


@app.command("serve")
def cmd_serve(
    host: Annotated[str, typer.Option("--host", help="Bind address.")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", help="TCP port.", min=1, max=65535)] = 8765,
    filename: FilenameOpt = None,
) -> None:
    """Run a small JSON HTTP API (requires: pip install 'wiseyoda[api]')."""
    try:
        import uvicorn
    except ImportError:
        console.print(
            "[red]uvicorn is required. Install with:[/red] pip install 'wiseyoda[api]'",
            file=sys.stderr,
        )
        raise typer.Exit(code=1) from None
    try:
        from .api import build_app
    except ImportError as e:
        console.print(
            f"[red]FastAPI import failed: {e}. Install with:[/red] pip install 'wiseyoda[api]'",
            file=sys.stderr,
        )
        raise typer.Exit(code=1) from e
    path = resolve_quotes_path(filename)
    api = build_app(quotes_path=path)
    uvicorn.run(api, host=host, port=port, log_level="info")


@app.command("version")
def cmd_version() -> None:
    """Print package version."""
    console.print(_pkg_version())


def run() -> None:
    app()


if __name__ == "__main__":
    run()
