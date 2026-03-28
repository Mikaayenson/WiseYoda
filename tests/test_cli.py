"""Smoke tests for the Typer CLI."""

from typer.testing import CliRunner
from wise_yoda.cli import app

runner = CliRunner()


def test_help() -> None:
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "wiseyoda" in r.stdout.lower() or "wisdom" in r.stdout.lower()


def test_version_subcommand() -> None:
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert r.stdout.strip()


def test_stats() -> None:
    r = runner.invoke(app, ["stats"])
    assert r.exit_code == 0
    assert "Total" in r.stdout or "season" in r.stdout.lower()


def test_search_no_results() -> None:
    r = runner.invoke(app, ["search", "zzzznotfoundzzz"])
    assert r.exit_code == 0
