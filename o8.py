import logging
import logging.config
import logging.handlers
import sys

from unitparsing_pkg.prices import (Bundle, CaculateUnitPriceException,
                                    ParseQuantityException, UnitPrice)

l1 = logging.getLogger("unitparsing_pkg.prices")
l1.setLevel(logging.DEBUG)

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setFormatter(formatter)

root.addHandler(handler)
l1.addHandler(handler)

for key in logging.Logger.manager.loggerDict:
    print(key)

root.debug("debug")
x = UnitPrice.unit_price("5.49/pt")
root.debug(x)
