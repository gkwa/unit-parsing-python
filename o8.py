import logging
import logging.config
import logging.handlers
import sys

from unitparsing_pkg.prices import (Bundle, CaculateUnitPriceException,
                                    ParseQuantityException, UnitPrice)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

UnitPrice.quantity("250ML")

