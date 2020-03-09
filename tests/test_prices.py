import pytest

from unitparsing_pkg.prices import (Bundle, CaculateUnitPriceException,
                                    ParseQuantityException, UnitPrice)


@pytest.mark.xfail
def test_quantity_without_number_more():
    assert Bundle(128, "oz") == UnitPrice.quantity("fl.gal")
    assert Bundle(128, "oz") == UnitPrice.quantity("  fl.  gal   ")
    assert Bundle(128, "oz") == UnitPrice.quantity("  fl.    gal   ")
    assert Bundle(1, "oz") == UnitPrice.quantity("fl.oz")
    assert Bundle(1, "oz") == UnitPrice.quantity("  fl.  oz   ")
    assert Bundle(1, "oz") == UnitPrice.quantity("  fl.    oz   ")


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Mission White Corn Tortillas - 30 Count", (30, "count")),
        (" 100 pack ", (100, "pack")),
        ("100pack", (100, "pack")),
        ("100 pk", (100, "pack")),
        ("2 ct", (2, "count")),
        ("1 ct", (1, "count")),
        ("1/2ct", (0.5, "count")),
        ("1/8count", (0.125, "count")),
        ("Coast Style Clam Chowder Soup 1/2 count 3/4 count", (0.5, "count"),),
        ("Pacific Coast Style Clam Chowder Soup 1/2 count", (0.5, "count")),
        ("Pacific Coast Style Clam Chowder Soup 1/2ct", (0.5, "count")),
        ("Pacific Coast Style Clam Chowder Soup - 23ct", (23, "count")),
        ("Pacific Coast Style Clam Chowder Soup - 23ct ", (23, "count")),
        ("Pacific Coast Style Clam Chowder Soup - 23 ct", (23, "count")),
        ("De Nigris Vinegar Balsamic Bronze Eagle - 16.9 Fl. Oz.", (16.9, "oz")),
        ("Seedless Mini Watermelon - 12 Each 13ea ", (12, "each")),
        ("Seedless Mini Watermelon - 12 Each 13 each", (12, "each")),
        ("Seedless Mini Watermelon - 12 Each", (12, "each")),
        ("Seedless Mini Watermelon - Each", (1, "each")),
        ("1.3 ea", (1.3, "each")),
        ("1 each", (1, "each")),
        ("each", (1, "each")),
        ("1each", (1, "each")),
        ("0.5pk", (0.5, "pack")),
        ("100 pk", (100, "pack")),
        ("1/2 pk", (0.5, "pack")),
        (".3pack ", (0.3, "pack")),
        ("1/2 pack ", (0.5, "pack")),
        ("Signature Cafe Pacific Coast Style Clam Chowder Soup - 24 Oz.", (24, "oz")),
        ("Azumaya Tofu Extra Firm - 14 Oz", (14, "oz")),
        ("Squid Whole Raw Frozen - 3.00Lb", (48, "oz")),
        ("Squid Whole Raw Frozen - 3.00 LB", (48, "oz")),
        ("Squid Whole Raw Frozen3.00Lb", (48, "oz")),
        ("ham sandwich 4 ct/15.25 oz", (61, "oz")),
        ("4 ct/15.25 oz", (61, "oz")),
        ("4 ct / 15.25 oz", (61, "oz")),
        ("1 lb", (16, "oz")),
        ("1/2 lb", (8, "oz")),
        ("1/2 oz ", (0.5, "oz")),
        ("1/2 / lb", (8, "oz")),
        ("1/2 /lb", (8, "oz")),
        ("10 oz", (10, "oz")),
        ("10 Oz", (10, "oz")),
        ("10.5 oz", (10.5, "oz")),
        ("14.75 oz", (14.75, "oz")),
        ("16 ct / 40 oz", (640, "oz")),
        ("24 ct / 50.8 oz", (1219.1999999999998, "oz")),
        ("1 pint", (16, "oz")),
        ("1  pint ", (16, "oz")),
        ("1 pt", (16, "oz")),
        ("1pint ", (16, "oz")),
        ("3.5 1/2 pints", (28, "oz")),
        ("3.5 1/2 pt", (28, "oz")),
        ("3/4 1/2 pt", (6, "oz")),
        ("3 1/2 pt", (24, "oz")),
        ("1/2pt", (8, "oz")),
        ("1/2 pt", (8, "oz")),
        ("1 quart", (32, "oz")),
        ("1  quart ", (32, "oz")),
        ("1 qt", (32, "oz")),
        ("1quart ", (32, "oz")),
        ("3.5 1/2 quarts", (56, "oz")),
        ("3.5 1/2 qt", (56, "oz")),
        ("3/4 1/2 qt", (12, "oz")),
        ("3 1/2 qt", (48, "oz")),
        ("1/2qt", (16, "oz")),
        ("1/2 qt", (16, "oz")),
        ("1 gallon", (128, "oz")),
        ("1  gallon ", (128, "oz")),
        ("1 gal", (128, "oz")),
        ("1gallon ", (128, "oz")),
        ("3.5 1/2 gallons", (224, "oz")),
        ("3.5 1/2 gal", (224, "oz")),
        ("3/4 1/2 gal", (48, "oz")),
        ("3 1/2 gal", (192, "oz")),
        ("1/2gal", (64, "oz")),
        ("1/2 gal", (64, "oz")),
        ("250ML", (250, "ml")),
        ("250 ml", (250, "ml")),
        ("Lawry's Signature Steakhouse Marinade - 12oz", (12, "oz")),
        ("Frozen Chicken Breast Tenderloins - 2.5lbs - Archer Farms™", (40, "oz")),
        ("Vegan Peach Ginger Kombucha - 15.2oz", (15.2, "oz")),
        ("Land O' Lakes Mini Half & Half - Serve Pods - 192ct/54 fl oz", (10368, "oz")),
        ("B-Tea Raw & Organic Green Tea - 6pk/16 fl oz Bottles", (96, "oz")),
        ("oZ   ", (1, "oz")),
        ("  LB   ", (16, "oz")),
        ("  gallons   ", (128, "oz")),
        ("floz", (1, "oz")),
        ("fl oz", (1, "oz")),
        ("fl  oz", (1, "oz")),
        ("fl  oz   ", (1, "oz")),
        ("  fl  oz   ", (1, "oz")),
        ("  fl    oz   ", (1, "oz")),
        ("flgal", (128, "oz")),
        ("fl gal", (128, "oz")),
        ("fl  gal", (128, "oz")),
        ("fl  gal   ", (128, "oz")),
        ("  fl  gal   ", (128, "oz")),
        ("  fl    gal   ", (128, "oz")),
    ],
)
def test_quantity(test_input, expected):
    amount, unit = expected[0], expected[1]
    assert Bundle(amount, unit) == UnitPrice.quantity(test_input)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1.99/bunch", (1.99, "bunch")),
        ("$7.99 / 300 ML", (0.026633333333333335, "ml")),
        ("$14.69 / 250 ML", (0.05876, "ml")),
        ("4.99/100 pk", (0.0499, "pack")),
        ("2.69/2 count", (1.345, "count")),
        ("2.69/2 count", (1.345, "count")),
        ("5.49per pt", (5.49, "pt")),
        ("5.49 per pt", (5.49, "pt")),
        ("5.49 // pt", (5.49, "pt")),
        ("5.49 - oz", (5.49, "oz")),
        ("5.49 / pt", (5.49, "pt")),
        ("5.49 / pint", (5.49, "pint")),
        ("5.49 / oz", (5.49, "oz")),
        ("5.49/lb", (0.343125, "oz")),
        ("5.49 each", (5.49, "each")),
        ("5.49 / each", (5.49, "each")),
        ("$5.49 / each", (5.49, "each")),
        ("5.49 /EACH", (5.49, "each")),
        ("5/EACH", (5, "each")),
        ("1.99/lb", (0.124375, "oz")),
        ("(2.29/lb)", (0.143125, "oz")),
        ("( 2.29 /lb)", (0.143125, "oz")),
        ("24.99/96 oz", (0.2603125, "oz")),
        ("  oZ   ", (1, "oz")),
        ("LB   ", (16, "oz")),
        ("gal   ", (128, "oz")),
    ],
)
def test_unit_price(test_input, expected):
    assert UnitPrice.unit_price(test_input) == expected


def test_unit_price():
    with pytest.raises(CaculateUnitPriceException):
        UnitPrice.unit_price(" / oz")
    with pytest.raises(CaculateUnitPriceException):
        UnitPrice.unit_price("/ oz")
    with pytest.raises(CaculateUnitPriceException):
        UnitPrice.unit_price("5.49 / ")


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
