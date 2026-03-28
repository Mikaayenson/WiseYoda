"""remind subcommand."""

from typer.testing import CliRunner
from wise_yoda.cli import app

runner = CliRunner()


def test_remind_random_includes_notification_commands() -> None:
    r = runner.invoke(app, ["remind", "-r"])
    assert r.exit_code == 0
    assert "osascript" in r.stdout
    assert "notify-send" in r.stdout
