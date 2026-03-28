"""Toy Yoda phrasing."""

from wise_yoda.yoda_style import to_yoda_speak


def test_comma_swap() -> None:
    out = to_yoda_speak("Hello, world.")
    assert "world" in out.lower()
    assert "hello" in out.lower()


def test_empty() -> None:
    assert to_yoda_speak("") == ""
    assert to_yoda_speak("   ") == ""
