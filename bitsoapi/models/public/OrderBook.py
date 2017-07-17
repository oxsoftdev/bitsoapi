import dateutil.parser
from decimal import Decimal

from .._BaseModel import BaseModel


class Order(BaseModel):

    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'book':
                setattr(self, 'book', value)
            elif param == 'price':
                setattr(self, 'price', Decimal(str(value)))
            elif param == 'amount':
                setattr(self, 'amount', Decimal(str(value)))
            elif param == 'oid':
                setattr(self, 'oid', value)

    def __repr__(self):
        return "Order({Order})".format(
            Order=self._repr('book', 'amount', 'price')
        )


class OrderBook(BaseModel):

    def __init__(self, **kwargs):
        self.asks=[]
        self.bids=[]
        self.updated_at=dateutil.parser.parse(kwargs.get('updated_at'))
        self.sequence=int(kwargs.get('sequence'))

        for order in kwargs.get('asks'):
            self.asks.append(Order._NewFromJsonDict(order))
        for order in kwargs.get('bids'):
            self.bids.append(Order._NewFromJsonDict(order))

    def __repr__(self):
        return "OrderBook({num_asks} asks, {num_bids} bids, updated_at={updated_at})".format(
            num_asks = len(self.asks),
            num_bids = len(self.bids),
            updated_at = self.updated_at)
