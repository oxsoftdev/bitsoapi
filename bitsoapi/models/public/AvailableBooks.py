from decimal import Decimal

from .._BaseModel import BaseModel


class Book(BaseModel):

    def __init__(self, **kwargs):
        for (param, value) in kwargs.items():
            if param == 'book':
                setattr(self, 'book', value)
            elif param == 'minimum_amount':
                setattr(self, 'minimum_amount', Decimal(str(value)))
            elif param == 'maximum_amount':
                setattr(self, 'maximum_amount', Decimal(str(value)))
            elif param == 'minimum_price':
                setattr(self, 'minimum_price', Decimal(str(value)))
            elif param == 'maximum_price':
                setattr(self, 'maximum_price', Decimal(str(value)))
            elif param == 'minimum_value':
                setattr(self, 'minimum_value', Decimal(str(value)))
            elif param == 'maximum_value':
                setattr(self, 'maximum_value', Decimal(str(value)))

    def __repr__(self):
        return "Book({Book})".format(
            Book=self._repr('book')
        )


class AvailableBooks(BaseModel):

    def __init__(self, **kwargs):
        self.books = []
        for ob in kwargs.get('payload'):
            self.books.append(ob['book'])
            setattr(self, ob['book'], Book._NewFromJsonDict(ob))

    def __repr__(self):
        return "AvailableBooks(books={books})".format(books=','.join(self.books))

