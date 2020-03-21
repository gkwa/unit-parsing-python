import pytest

from unitparsing_pkg.prices import Bundle, ParseQuantityException, UnitPrice

test_quantity_parameter_list_expected_fail_list = [
    ("fl.gal", (128, "oz")),
    ("  fl.  gal   ", (128, "oz")),
]


@pytest.mark.parametrize(
    "test_input,expected", test_quantity_parameter_list_expected_fail_list
)
def test_quantity_without_number_more(test_input, expected):
    amount, unit = expected[0], expected[1]
    with pytest.raises((ParseQuantityException, ValueError)):
        assert Bundle(amount, unit) == UnitPrice.quantity(test_input)
