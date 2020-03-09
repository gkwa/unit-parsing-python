"""
>>> b = UnitPrice.quantity("1/2 / lb")
>>> b.amount
8.0
>>> b.unit
'oz'
>>> b.unit=='oz'
True
>>> from unitparsing_pkg.prices import Bundle, UnitPrice
>>> Bundle(8, "oz") == UnitPrice.quantity("1/2 / lb")
True
"""

import fractions
import logging
import pathlib
import pprint
import re


class ParseQuantityException(Exception):
    """Base class for other exceptions"""


class CaculateUnitPriceException(Exception):
    """Base class for other exceptions"""


class Bundle:
    def __init__(self, amount, unit):
        self.logger = logging.getLogger(__name__)
        self.amount = amount
        self.unit = unit

    def __repr__(self):
        return f"Bundle({self.amount!r}, {self.unit!r})"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Bundle):
            return (self.amount == other.amount) and (self.unit == other.unit)

        return False


class UnitPrice:
    logger = logging.getLogger(__name__)

    OZ_PER_LB = 16
    OZ_PER_PINT = 16
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

    # 1/2 oz
    # 32 oz
    pat_oz_2 = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        OZ\b
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

    pat_multi = re.compile(
        r"""
        .*?
        \s*
        ((?P<num>[\.\d/]+)\s+)?
        \s*
        (?P<qty>[\.\d/]+)
        \s*
        (?P<unit>
          pts?\b | pints?\b
        | mls?\b | milliliters?\b
        | qt\b | quarts?\b
        | gal\b | gallons?\b
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # no number, assume 1
    pat_no_number_multi = re.compile(
        r"""
        [^\d\.]*
        \s*
        (?P<unit> 
          LBs?\b | pounds?\b
          | OZs?\b | ounces?\b
          | gals?\b | gallons?\b
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # each
    pat_each_2 = re.compile(
        r"""
        .*?
        [^\d\.]?
        \s*
        \bEach\b
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

    # 4 ct / 15.25 oz
    # 15 cans / 12 fl oz
    # 6pk/16 fl oz Bottles
    pat_can = re.compile(
        r"""
        .*?
        (?P<num>[\.\d/]+)
        \s*
        (?:ct|count|cans?|jars?|pks?|pack)
        \s*
        /
        \s*
        (?P<qty>[\.\d/]+)
        \s*
        (FL\.?)?
        \s*
        OZ\b
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
    # 1/2 lbs
    # 1/2 lb
    pat_lb = re.compile(
        r"""
        .*?
        (?P<qty>[\.\d/]+)
        \s*
        /?
        \s*
        LBs?\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    pat_unit_price = re.compile(
        r"""
        .*?
        (?P<dollars>[\.\d]+)
        \s*
        (?:
        / | per | -
        )*
        \s*
        (?P<qty>[\.\d]+)?
        \s*
        (?P<unit>
        lb 
        | oz 
        | \bbunch\b
        | \bpk\b | \bpack\b
        | \bct\b | \bcount\b
        | \bmls?\b | \bmilliliters?\b
        | \bea\b | \beach\b
        | \bpint\b | \bpt\b
        )
        """,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    @classmethod
    def _convert_oz(cls, qty, unit):
        if unit == "lb":
            qty /= cls.OZ_PER_LB
            unit = "oz"
            return qty, unit
        return qty, unit

    @classmethod
    def unit_price(cls, text):
        orig = text
        text = str(text)  # text might not be string, could be float, int
        text = text.lower()
        if match := re.match(cls.pat_unit_price, text):
            dollars = float(match.group("dollars"))
            qty = float(match.group("qty") or 1)
            unit = match.group("unit")
            if unit:
                unit = unit.lower().strip()
                if unit in ["pk", "pack"]:
                    unit = "pack"
                elif unit in ["bunch"]:
                    unit = "bunch"
            qty, unit = cls._convert_oz(dollars / qty, unit)
            return (qty, unit)
        raise CaculateUnitPriceException(
            f"can't generate unit price from text '{orig}'"
        )

    @classmethod
    def doit(cls, number, qty, unit):
        unit = unit.lower().strip()
        if unit in ["pt", "pint", "pints"]:
            result = Bundle(number * qty * cls.OZ_PER_PINT, "oz")
        elif unit in ["ml", "mls", "milliliter", "milliliters"]:
            result = Bundle(number * qty, "ml")
        elif unit in ["qt", "quart", "quarts"]:
            result = Bundle(number * qty * cls.OZ_PER_QUART, "oz")
        elif unit in ["fl.gal", "flgal", "gal", "gals", "gallon", "gallons"]:
            result = Bundle(number * qty * cls.OZ_PER_GAL, "oz")
        elif unit in ["lb", "lbs", "pound", "pounds"]:
            result = Bundle(number * qty * cls.OZ_PER_LB, "oz")
        elif unit in ["fl.oz", "floz", "oz", "ozs", "ounce", "ounces"]:
            result = Bundle(number * qty, "oz")
        else:
            raise ValueError("something went wrong with pat_pint_quart parsing")

        return result

    @classmethod
    def quantity(cls, text):
        def frac(str_):
            """ 1/2 to 0.5 """
            return float(sum(fractions.Fraction(s) for s in str_.split()))

        text = "" if text is None else text

        if not isinstance(text, str):
            pf = pprint.pformat(text)
            raise ParseQuantityException(
                f"I'm expecting a string for text '{text}' but faound a {type(text)} instead"
            )

        result = None
        if match := re.match(cls.pat_oz_4, text):
            cls.logger.debug("regex matches on 'pat_oz_4'")
            qty = frac(match.group("qty"))
            number = float(match.group("num"))
            result = Bundle(qty * number, "oz")

        elif match := re.match(cls.pat_multi, text):
            cls.logger.debug("regex matches on 'pat_multi'")
            number = float(frac(match.group("num") or "1"))
            qty = frac(match.group("qty") or "1")
            unit = match.group("unit").strip()
            return cls.doit(number, qty, unit)

        elif match := re.match(cls.pat_no_number_multi, text):
            cls.logger.debug("regex matches on 'pat_no_number_multi'")
            number = 1
            qty = 1
            unit = match.group("unit").strip()
            return cls.doit(number, qty, unit)

        elif match := re.match(cls.pat_bunch, text):
            cls.logger.debug("regex matches on 'pat_bunch'")
            qty = frac(match.group("qty"))
            result = Bundle(qty, "bunch")

        elif match := re.match(cls.pat_can, text):
            cls.logger.debug("regex matches on 'pat_can'")
            qty = frac(match.group("qty"))
            number = frac(match.group("num"))
            result = Bundle(qty * number, "oz")

        elif match := re.match(cls.pat_count, text):
            cls.logger.debug("regex matches on 'pat_count'")
            qty = frac(match.group("qty"))
            result = Bundle(qty, "count")

        elif match := re.match(cls.pat_each, text):
            cls.logger.debug("regex matches on 'pat_each'")
            qty = frac(match.group("qty"))
            result = Bundle(qty, "each")

        elif match := re.match(cls.pat_gallon_2, text):
            cls.logger.debug("regex matches on 'pat_gallon_2'")
            qty = frac(match.group("qty") or "1")
            result = Bundle(qty * 0.5 * cls.OZ_PER_GAL, "oz")

        elif match := re.match(cls.pat_lb, text):
            cls.logger.debug("regex matches on 'pat_lb'")
            qty = frac(match.group("qty"))
            result = Bundle(qty * cls.OZ_PER_LB, "oz")

        elif match := re.match(cls.pat_oz_3, text):
            cls.logger.debug("regex matches on 'pat_oz_3'")
            qty = frac(match.group("qty"))
            result = Bundle(qty, "oz")

        elif match := re.match(cls.pat_oz_2, text):
            cls.logger.debug("regex matches on 'pat_oz_2'")
            qty = frac(match.group("qty"))
            result = Bundle(qty, "oz")

        elif match := re.match(cls.pat_oz_5, text):
            cls.logger.debug("regex matches on 'pat_oz_5'")
            qty = frac(match.group("qty"))
            number = float(match.group("num"))
            result = Bundle(qty * number, "oz")

        elif match := re.match(cls.pat_each_2, text):
            cls.logger.debug("regex matches on 'pat_each_2'")
            result = Bundle(1, "each")

        elif match := re.match(cls.pat_pack, text):
            cls.logger.debug("regex matches on 'pat_pack'")
            qty = frac(match.group("qty"))
            result = Bundle(qty, "pack")

        else:
            raise ParseQuantityException(f"can't match quantity on string '{text}'")

        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
