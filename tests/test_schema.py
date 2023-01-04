"""Test the schema."""
from wise_yoda.wisdom import QUOTELISTSCHEMA, QUOTESCHEMA


def test_schema_loads(quote_data):
    """Test the schema loads."""
    data = quote_data.get("data")[0]
    quote = QUOTESCHEMA.load(data)
    assert quote.title == "Ambush"
    assert quote.description == "Great leaders inspire greatness in others."
    assert quote.season == 1
    assert quote.episode == 1


def test_schema_dumps(quote_data):
    """Test the schema dumps."""
    data = quote_data.get("data")[0]
    quote = QUOTESCHEMA.load(data)
    result = QUOTESCHEMA.dump(quote)
    assert result == data


def test_schema_loads_list(quote_data):
    """Test the schema loads a list."""
    quotes = QUOTELISTSCHEMA.load(quote_data)
    assert len(quotes.data) == 2
    assert quotes.data[0].title == "Ambush"
    assert quotes.data[0].description == "Great leaders inspire greatness in others."
    assert quotes.data[0].season == 1
    assert quotes.data[0].episode == 1
    assert quotes.data[1].title == "Rising Malevolence"
    assert quotes.data[1].description == "Fear is the path to the dark side. Fear leads to anger."
    assert quotes.data[1].season == 2
    assert quotes.data[1].episode == 1
