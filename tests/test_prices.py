import pytest

from unitparsing_pkg.prices import (Bundle, CaculateUnitPriceException,
                                    ParseQuantityException, UnitPrice)


def test_unit_price():
    with pytest.raises(CaculateUnitPriceException):
        UnitPrice.unit_price(" / oz")
    with pytest.raises(CaculateUnitPriceException):
        UnitPrice.unit_price("/ oz")

    assert (0.026633333333333335, "ml") == UnitPrice.unit_price("$7.99 / 300 ML")
    assert (0.05876, "ml") == UnitPrice.unit_price("$14.69 / 250 ML")
    assert (0.0499, "each") == UnitPrice.unit_price("4.99/100 pk")
    assert (1.345, "count") == UnitPrice.unit_price("2.69/2 count")
    assert (1.345, "count") == UnitPrice.unit_price("2.69/2 count")
    assert (5.49, "pt") == UnitPrice.unit_price("5.49per pt")
    assert (5.49, "pt") == UnitPrice.unit_price("5.49 per pt")
    assert (5.49, "pt") == UnitPrice.unit_price("5.49 // pt")
    assert (5.49, "oz") == UnitPrice.unit_price("5.49 - oz")
    assert (5.49, "pt") == UnitPrice.unit_price("5.49 / pt")
    assert (5.49, "pint") == UnitPrice.unit_price("5.49 / pint")
    with pytest.raises(CaculateUnitPriceException):
        UnitPrice.unit_price("5.49 / ")
    assert (5.49, "oz") == UnitPrice.unit_price("5.49 / oz")
    assert (0.343125, "oz") == UnitPrice.unit_price("5.49/lb")
    assert (5.49, "each") == UnitPrice.unit_price("5.49 each")
    assert (5.49, "each") == UnitPrice.unit_price("5.49 / each")
    assert (5.49, "each") == UnitPrice.unit_price("$5.49 / each")
    assert (5.49, "each") == UnitPrice.unit_price("5.49 /EACH")
    assert (5, "each") == UnitPrice.unit_price("5/EACH")


def test_multiple_quantities_in_one_string_will_take_the_first_pair():
    assert Bundle(61, "oz") == UnitPrice.quantity("4 ct / 15.25 oz 5 ct / 15.25 oz")


def test_fraction_without_spaces_causes_exception():
    with pytest.raises(ValueError):
        UnitPrice.quantity("1/2/lb")

    with pytest.raises(ValueError):
        UnitPrice.quantity("1/2/ lb")


def test_missing_units_should_raise_exception():
    with pytest.raises(ParseQuantityException):
        UnitPrice.quantity("1.3 easter egg")

    with pytest.raises(ParseQuantityException):
        UnitPrice.quantity(
            "Signature Cafe Pacific Coast Style Clam Chowder Soup - 23c "
        )


def test_getting_quantity_from_empty_string():
    with pytest.raises(ParseQuantityException):
        UnitPrice.quantity(None)


def test_quantity_with_assert_equals():
    with pytest.raises(ParseQuantityException):
        UnitPrice.quantity("1.3 cantspell")


@pytest.mark.skip(reason="not sure how to handle this one")
def test_many_strings():
    str_ = """Kroger® Sweet Golden Whole Kernel Corn - No Salt Added"""


def test_quantity():
    assert Bundle(30, "count") == UnitPrice.quantity(
        "Mission White Corn Tortillas - 30 Count"
    )
    assert Bundle(100, "pack") == UnitPrice.quantity(" 100 pack ")
    assert Bundle(100, "pack") == UnitPrice.quantity("100pack")
    assert Bundle(100, "pack") == UnitPrice.quantity("100 pk")
    assert Bundle(2, "count") == UnitPrice.quantity("2 ct")
    assert Bundle(1, "count") == UnitPrice.quantity("1 ct")
    assert Bundle(0.5, "count") == UnitPrice.quantity("1/2ct")
    assert Bundle(0.125, "count") == UnitPrice.quantity("1/8count")
    assert Bundle(0.5, "count") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup 1/2 count 3/4 count"
    )
    assert Bundle(0.5, "count") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup 1/2 count"
    )
    assert Bundle(0.5, "count") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup 1/2ct"
    )
    assert Bundle(23, "count") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup - 23ct"
    )
    assert Bundle(23, "count") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup - 23ct "
    )
    assert Bundle(23, "count") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup - 23 ct"
    )

    assert Bundle(12, "each") == UnitPrice.quantity(
        "Seedless Mini Watermelon - 12 Each 13ea "
    )
    assert Bundle(12, "each") == UnitPrice.quantity(
        "Seedless Mini Watermelon - 12 Each 13 each"
    )
    assert Bundle(12, "each") == UnitPrice.quantity(
        "Seedless Mini Watermelon - 12 Each"
    )
    assert Bundle(1, "each") == UnitPrice.quantity("Seedless Mini Watermelon - Each")
    assert Bundle(1.3, "each") == UnitPrice.quantity("1.3 ea")
    assert Bundle(1, "each") == UnitPrice.quantity("1 each")
    assert Bundle(1, "each") == UnitPrice.quantity("each")
    assert Bundle(1, "each") == UnitPrice.quantity("1each")

    assert Bundle(0.5, "pack") == UnitPrice.quantity("0.5pk")
    assert Bundle(100, "pack") == UnitPrice.quantity("100 pk")
    assert Bundle(0.5, "pack") == UnitPrice.quantity("1/2 pk")
    assert Bundle(0.3, "pack") == UnitPrice.quantity(".3pack ")
    assert Bundle(0.5, "pack") == UnitPrice.quantity("1/2 pack ")

    assert Bundle(24, "oz") == UnitPrice.quantity(
        "Signature Cafe Pacific Coast Style Clam Chowder Soup - 24 Oz."
    )
    assert Bundle(14, "oz") == UnitPrice.quantity("Azumaya Tofu Extra Firm - 14 Oz")
    assert Bundle(48, "oz") == UnitPrice.quantity("Squid Whole Raw Frozen - 3.00Lb")
    assert Bundle(48, "oz") == UnitPrice.quantity("Squid Whole Raw Frozen - 3.00 LB")
    assert Bundle(48, "oz") == UnitPrice.quantity("Squid Whole Raw Frozen3.00Lb")
    assert Bundle(61, "oz") == UnitPrice.quantity("ham sandwich 4 ct/15.25 oz")
    assert Bundle(61, "oz") == UnitPrice.quantity("4 ct/15.25 oz")
    assert Bundle(61, "oz") == UnitPrice.quantity("4 ct / 15.25 oz")
    assert Bundle(16, "oz") == UnitPrice.quantity("1 lb")
    assert Bundle(8, "oz") == UnitPrice.quantity("1/2 lb")
    assert Bundle(0.5, "oz") == UnitPrice.quantity("1/2 oz ")
    assert Bundle(8, "oz") == UnitPrice.quantity("1/2 / lb")
    assert Bundle(8, "oz") == UnitPrice.quantity("1/2 /lb")
    assert Bundle(10, "oz") == UnitPrice.quantity("10 oz")
    assert Bundle(10, "oz") == UnitPrice.quantity("10 Oz")
    assert Bundle(10.5, "oz") == UnitPrice.quantity("10.5 oz")
    assert Bundle(14.75, "oz") == UnitPrice.quantity("14.75 oz")
    assert Bundle(640, "oz") == UnitPrice.quantity("16 ct / 40 oz")
    assert Bundle(1219.1999999999998, "oz") == UnitPrice.quantity("24 ct / 50.8 oz")

    assert Bundle(16, "oz") == UnitPrice.quantity("1 pint")
    assert Bundle(16, "oz") == UnitPrice.quantity("1  pint ")
    assert Bundle(16, "oz") == UnitPrice.quantity("1 pt")
    assert Bundle(16, "oz") == UnitPrice.quantity("1pint ")
    assert Bundle(28, "oz") == UnitPrice.quantity("3.5 1/2 pints")
    assert Bundle(28, "oz") == UnitPrice.quantity("3.5 1/2 pt")
    assert Bundle(6, "oz") == UnitPrice.quantity("3/4 1/2 pt")
    assert Bundle(24, "oz") == UnitPrice.quantity("3 1/2 pt")
    assert Bundle(8, "oz") == UnitPrice.quantity("1/2pt")
    assert Bundle(8, "oz") == UnitPrice.quantity("1/2 pt")

    assert Bundle(32, "oz") == UnitPrice.quantity("1 quart")
    assert Bundle(32, "oz") == UnitPrice.quantity("1  quart ")
    assert Bundle(32, "oz") == UnitPrice.quantity("1 qt")
    assert Bundle(32, "oz") == UnitPrice.quantity("1quart ")
    assert Bundle(56, "oz") == UnitPrice.quantity("3.5 1/2 quarts")
    assert Bundle(56, "oz") == UnitPrice.quantity("3.5 1/2 qt")
    assert Bundle(12, "oz") == UnitPrice.quantity("3/4 1/2 qt")
    assert Bundle(48, "oz") == UnitPrice.quantity("3 1/2 qt")
    assert Bundle(16, "oz") == UnitPrice.quantity("1/2qt")
    assert Bundle(16, "oz") == UnitPrice.quantity("1/2 qt")

    assert Bundle(128, "oz") == UnitPrice.quantity("1 gallon")
    assert Bundle(128, "oz") == UnitPrice.quantity("1  gallon ")
    assert Bundle(128, "oz") == UnitPrice.quantity("1 gal")
    assert Bundle(128, "oz") == UnitPrice.quantity("1gallon ")
    assert Bundle(224, "oz") == UnitPrice.quantity("3.5 1/2 gallons")
    assert Bundle(224, "oz") == UnitPrice.quantity("3.5 1/2 gal")
    assert Bundle(48, "oz") == UnitPrice.quantity("3/4 1/2 gal")
    assert Bundle(192, "oz") == UnitPrice.quantity("3 1/2 gal")
    assert Bundle(64, "oz") == UnitPrice.quantity("1/2gal")
    assert Bundle(64, "oz") == UnitPrice.quantity("1/2 gal")

    assert Bundle(250, "ml") == UnitPrice.quantity("250ML")
    assert Bundle(250, "ml") == UnitPrice.quantity("250 ml")
