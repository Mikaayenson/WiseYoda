"""export and pipe subcommands."""

import json

from typer.testing import CliRunner
from wise_yoda.cli import app

runner = CliRunner()


def test_export_markdown_header() -> None:
    r = runner.invoke(app, ["export", "markdown"])
    assert r.exit_code == 0
    assert "# WiseYoda export" in r.stdout


def test_export_csv_header() -> None:
    r = runner.invoke(app, ["export", "csv"])
    assert r.exit_code == 0
    assert "season,episode,title,description" in r.stdout.splitlines()[0]


def test_export_bad_format() -> None:
    r = runner.invoke(app, ["export", "xml"])
    assert r.exit_code == 1


def test_pipe_valid_json() -> None:
    payload = {
        "season": 1,
        "episode": 1,
        "title": "T",
        "description": "Hello, world.",
    }
    r = runner.invoke(app, ["pipe"], input=json.dumps(payload))
    assert r.exit_code == 0
    assert "world" in r.stdout or "Hello" in r.stdout


def test_pipe_empty_stdin() -> None:
    r = runner.invoke(app, ["pipe"], input="")
    assert r.exit_code == 1
