# Example
```
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
```
