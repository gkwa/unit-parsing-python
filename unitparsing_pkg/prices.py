"""
>>> b = UnitPrice().quantity("1/2 / lb")
>>> b.amount
8.0
>>> b.unit
'oz'
>>> b.unit=='oz'
True
>>> from unitparsing_pkg.prices import Bundle, UnitPrice
>>> Bundle(8, "oz") == UnitPrice().quantity("1/2 / lb")
True
"""

import fractions
import logging
import pathlib
import re


class Bundle:
    def __init__(self, amount, unit):
        self.amount = amount
        self.unit = unit

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Bundle):
            return (self.amount == other.amount) and (self.unit == other.unit)

        return False


class UnitPrice:
    OZ_PER_LB = 16
    OZ_PER_QUART = 32
    OZ_PER_GAL = 128
    ML_PER_OZ = 29.5735

    # 0.5pack
    # 2.5 pack
    # 1/2 pack
    # 100 pk
    pat_pack = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        (?:pack|pk)\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # no number, assume 1
    pat_lb_4 = re.compile(
        r"""
        [^\d\.]+
        \s*
        LB\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 1/2 oz
    # 32 oz
    pat_oz_2 = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        \bOZ\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 3.4 Fl Oz
    pat_oz_3 = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d]+)
        \s*
        Fl\.?
        \s*
        \bOZ\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # - 15-11 Fl Oz cans
    # - 6-11.2 Fl. Oz.
    pat_oz_4 = re.compile(
        r"""
        .*?
        \s+-\s+
        (?P<num>[\.\d]+)
        \s*
        -
        \s*
        (?P<qty>[\.\d]+)
        \s*
        Fl\.?
        \s*
        OZ\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 3 cans / 23 fl oz
    # 6 Count/11 Fl Oz
    pat_oz_5 = re.compile(
        r"""
        .*?
        (?P<num>[\.\d]+)
        \s*
        (?:cans?|ct|Count)
        \s*
        /
        \s*
        (?P<qty>[\.\d]+)
        \s*
        Fl.*?OZ
        \b""",
        re.IGNORECASE | re.VERBOSE,
    )

    # 3.2 Gal
    # 10 Gallons
    # 1/2 Gal
    pat_gallon_1 = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        (?:Gallon|Gal)
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 3 half gal
    pat_gallon_2 = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d]+)?
        \s*
        Half
        \s*
        (?:Gallon|Gal)
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 3 quarts
    pat_quart = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        Quarts?
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # each
    pat_each_2 = re.compile(
        r"""
        .*?
        [^\d\.]+
        \s*
        Each
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 10 bunch
    pat_bunch = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d]+)
        \s*
        /?
        \s*
        bunch
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 750 mL
    pat_ml = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d]+)
        \s
        *mL
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 4 ct / 15.25 oz
    # 15 cans / 12 fl oz
    pat_can = re.compile(
        r"""
        .*?
        (?P<num>[\.\d/]+)
        \s*
        (?:ct|count|cans?|jars?)
        \s*
        /
        \s*
        (?P<qty>[\.\d/]+)
        \s*
        (FL\.?)?
        \s*
        OZ
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # 3ea
    # 3 ea
    # 3 each
    # 3 / each
    # 3 Count
    # 3 ct
    pat_each = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        /?
        \s*
        (?:Each|ea)
        \b""",
        re.IGNORECASE | re.VERBOSE,
    )

    # 3 Count
    # 3 ct
    pat_count = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        /?
        \s*
        (?:Count|ct)
        \b""",
        re.IGNORECASE | re.VERBOSE,
    )

    # 3 lb
    # 3.4 / lb
    # 1/2 lb
    pat_lb = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        /?
        \s*
        LB\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    @classmethod
    def quantity(cls, text):
        def frac(str_):
            """ 1/2 to 0.5 """
            return float(sum(fractions.Fraction(s) for s in str_.split()))

        result = None
        if match := re.match(cls.pat_oz_4, text):
            qty = frac(match.group("qty"))
            number = float(match.group("num"))
            result = Bundle(qty * number, "oz")

        elif match := re.match(cls.pat_pack, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty, "pack")

        elif match := re.match(cls.pat_bunch, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty, "bunch")

        elif match := re.match(cls.pat_can, text):
            qty = frac(match.group("qty"))
            number = frac(match.group("num"))
            result = Bundle(qty * number, "oz")

        elif match := re.match(cls.pat_count, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty, "count")

        elif match := re.match(cls.pat_each, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty, "each")

        elif match := re.match(cls.pat_each_2, text):
            result = Bundle(1, "each")

        elif match := re.match(cls.pat_gallon_1, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty * cls.OZ_PER_GAL, "oz")

        elif match := re.match(cls.pat_gallon_2, text):
            qty = frac(match.group("qty")) or 1
            result = Bundle(qty * 0.5 * cls.OZ_PER_GAL, "oz")

        elif match := re.match(cls.pat_lb, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty * cls.OZ_PER_LB, "oz")

        elif match := re.match(cls.pat_lb_4, text):
            result = Bundle(1 * cls.OZ_PER_LB, "oz")

        elif match := re.match(cls.pat_ml, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty * cls.ML_PER_OZ, "oz")

        elif match := re.match(cls.pat_oz_2, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty, "oz")

        elif match := re.match(cls.pat_oz_3, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty, "oz")

        elif match := re.match(cls.pat_oz_5, text):
            qty = frac(match.group("qty"))
            number = float(match.group("num"))
            result = Bundle(qty * number, "oz")

        elif match := re.match(cls.pat_quart, text):
            qty = frac(match.group("qty"))
            result = Bundle(qty * cls.OZ_PER_QUART, "oz")

        else:
            raise ValueError(f"can't match quantity on string '{text}'")

        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
