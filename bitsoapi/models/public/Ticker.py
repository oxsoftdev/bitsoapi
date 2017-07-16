import dateutil.parser
from decimal import Decimal

from .._BaseModel import BaseModel


class Ticker(BaseModel):

    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'book':
                setattr(self, 'book', value)
            elif param == 'volume':
                setattr(self, 'volume', Decimal(str(value)))
            elif param == 'high':
                setattr(self, 'high', Decimal(str(value)))
            elif param == 'last':
                setattr(self, 'last', Decimal(str(value)))
            elif param == 'low':
                setattr(self, 'low', Decimal(str(value)))
            elif param == 'vwap':
                setattr(self, 'vwap', Decimal(str(value)))
            elif param == 'ask':
                setattr(self, 'ask', Decimal(str(value)))
            elif param == 'bid':
                setattr(self, 'bid', Decimal(str(value)))
            elif param == 'created_at':
                setattr(self, 'created_at', dateutil.parser.parse(value))

    def __repr__(self):
        return "Ticker({Ticker})".format(
            Ticker=self._repr('book', 'volume', 'last')
        )

