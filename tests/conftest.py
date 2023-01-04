"""Pytest configuration file."""
import pytest


@pytest.fixture(scope="module")
def quote_data():
    """Return a quote data test dict."""
    data = {
        "data": [
            {
                "title": "Ambush",
                "episode": 1,
                "season": 1,
                "description": "Great leaders inspire greatness in others.",
            },
            {
                "title": "Rising Malevolence",
                "episode": 1,
                "season": 2,
                "description": "Fear is the path to the dark side. Fear leads to anger.",
            },
        ]
    }
    return data
