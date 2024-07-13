from decimal import Decimal

from beancount.core.amount import Amount, sortkey, CURRENCY_RE
from beancount.core.display_context import DEFAULT_FORMATTER
from beancount.core.number import ZERO, D


class TotalPrice(Amount):
    """A 'TotalPrice' represents a number of a particular unit of something.

    It's essentially a typed number, with corresponding manipulation operations
    defined on it.
    """

    def __new__(cls, total, currency, count=None, per_unit=None):
        """Constructor from a number and currency.

        Args:
          total: A Decimal instance.
          currency: A string, the currency symbol to use.
          per_unit: A Decimal instance.
        """
        assert isinstance(total, Amount.valid_types_number), repr(total)
        assert isinstance(currency, Amount.valid_types_currency), repr(currency)

        if count is None and per_unit is None:
            per_unit = ZERO
        elif count is not None:
            assert isinstance(count, Amount.valid_types_number), repr(count)
            per_unit = ZERO if count == ZERO else total / count
        elif per_unit is not None:
            assert isinstance(per_unit, Amount.valid_types_number), repr(per_unit)

        amount = super().__new__(cls, per_unit, currency)
        amount.total = total
        return amount

    def __copy__(self):
        return type(self)(self.total, self.currency, None, self.number)

    def __deepcopy__(self, memodict={}):
        return self.__copy__()

    def to_total_string(self, dformat=DEFAULT_FORMATTER):
        """Convert an Amount instance to a printable string.

        Args:
          dformat: An instance of DisplayFormatter.
        Returns:
          A formatted string of the quantized amount and symbol.
        """
        number_fmt = (dformat.format(self.total, self.currency)
                      if isinstance(self.total, Decimal)
                      else str(self.total))
        return "{} {}".format(number_fmt, self.currency)

    def __neg__(self):
        raise NotImplementedError("A TotalPrice may not be negated")
