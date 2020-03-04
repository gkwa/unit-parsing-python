import pytest

from unitparsing_pkg.prices import Bundle, ParseQuantityException, UnitPrice


def test_unit_price():
    with pytest.raises(ValueError):
        UnitPrice().unit_price("per 3 oz")
    assert (5.49, "pt") == UnitPrice().unit_price("5.49per pt")


def test_multiple_quantities_in_one_string_will_take_the_first_pair():
    assert Bundle(61, "oz") == UnitPrice().quantity("4 ct / 15.25 oz 5 ct / 15.25 oz")


def test_missing_units_should_raise_exception():
    with pytest.raises(ParseQuantityException):
        UnitPrice().quantity("1.3 easter egg")

    with pytest.raises(ParseQuantityException):
        UnitPrice().quantity(
            "Signature Cafe Pacific Coast Style Clam Chowder Soup - 23c "
        )


@pytest.mark.skip(reason="not sure how to handle this one")
def test_many_strings():
    str_ = """Kroger® Sweet Golden Whole Kernel Corn - No Salt Added"""
    # not done with this yet, skip it

def test_quantity():
    assert Bundle(30, "count") == UnitPrice().quantity(
        "Mission White Corn Tortillas - 30 Count"
    )
    assert Bundle(1, "each") == UnitPrice().quantity("Seedless Mini Watermelon - Each")

