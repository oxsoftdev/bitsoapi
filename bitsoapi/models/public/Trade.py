import dateutil.parser
from decimal import Decimal

from .._BaseModel import BaseModel


class Trade(BaseModel):

    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'book':
                setattr(self, 'book', value)
            elif param == 'created_at':
                setattr(self, 'created_at', dateutil.parser.parse(value))
            elif param == 'amount':
                setattr(self, 'amount', Decimal(str(value)))
            elif param == 'maker_side':
                setattr(self, 'maker_side', value)
            elif param == 'price':
                setattr(self, 'price', Decimal(str(value)))
            elif param == 'tid':
                setattr(self, 'tid', value)

    def __repr__(self):
        return "Trade({Trade})".format(
            Trade=self._repr('book', 'tid', 'amount', 'price')
        )
