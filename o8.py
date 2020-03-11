import logging
import sys

from unitparsing_pkg.prices import Bundle, UnitPrice

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

b = Bundle(61, "oz")

v = UnitPrice.quantity("250ML")
logger.debug(v)

v = UnitPrice.unit_price("2.19/qt")
