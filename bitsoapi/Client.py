from .errors import (ApiError, ApiClientError)
from .mixins import ApiClientMixin
from .models.public import (
    AvailableBooks
    , Ticker
    , OrderBook
    , Trade
)


class Client(ApiClientMixin):

    def __init__(self, key=None, secret=None):
        self.base_url = 'https://bitso.com/api/v3'
        self.key = key
        self._secret = secret

    # public api

    def available_books(self):
        url = '%s/available_books/' % self.base_url
        resp = self._request_url(url, 'GET')
        return AvailableBooks(resp)

    def ticker(self, book):
        url = '%s/ticker/' % self.base_url
        parameters = {}
        parameters['book'] = book
        resp = self._request_url(url, 'GET', params=parameters)
        return Ticker(resp['payload'])

    def order_book(self, book, aggregate=True):
        url = '%s/order_book/' % self.base_url
        parameters = {}
        parameters['book'] = book
        parameters['aggregate'] = aggregate
        resp = self._request_url(url, 'GET', params=parameters)
        return OrderBook(resp['payload'])

    def trades(self, book, **kwargs):
        url = '%s/trades/' % self.base_url
        parameters = {}
        parameters['book'] = book
        if 'marker' in kwargs:
            parameters['marker'] = kwargs['marker']
        if 'limit' in kwargs:
            parameters['limit'] = kwargs['limit']
        else:
            parameters['limit'] = 100
        if 'sort' in kwargs:
            parameters['sort'] = kwargs['sort']
        resp = self._request_url(url, 'GET', params=parameters)
        return [Trade(o) for o in resp['payload']]

    # private api
    
    def account_status(self):
        url = '%s/account_status/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        return AccountStatus(resp['payload'])
    
    def balance(self):
        url = '%s/balance/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        return Balance(resp['payload'])
    
    def fees(self):
        url = '%s/fees/' % self.base_url
        resp = self._request_url(url, 'GET', private=True)
        return Fees(resp['payload'])
    
    def ledger(self, operation='', marker=None, limit=25, sort='desc'):
        _operations = ['', 'trades', 'fees', 'fundings', 'withdrawals']
        if not isinstance(operation, str) and operation not in _operations:
            raise ApiClientError({'message': 'invalid operation'})
        url = '%s/ledger/%s' % (self.base_url, operation)
        parameters = {}
        if marker:
            parameters['marker'] = marker
        if limit:
            parameters['limit'] = limit
        if sort:
            parameters['sort'] = sort
        resp = self._request_url(url, 'GET', params=parameters, private=True)
        return [LedgerEntry(o) for entry in resp['payload']]

    def withdrawals(self):
        raise NotImplementedError

    def fundings(self):
        raise NotImplementedError

    def user_trades(self, tids=[], book=None, marker=None, limit=25, sort='desc'):
        raise NotImplementedError

    def order_trades(self, oid):
        raise NotImplementedError

    def open_orders(self, book=None):
        raise NotImplementedError

    def lookup_orders(self, oids):
        raise NotImplementedError

    def cancel_orders(self, oids):
        if isinstance(oids, str):
            oids = [oids]
        url = '%s/orders/' % self.base_url
        url+= '%s/' % ('-'.join(oids))
        resp = self._request_url(url, 'DELETE', private=True)
        return resp['payload']

    def place_order(self, book, side, type, **kwargs):
        _sides = ['buy', 'sell']
        _types = ['market', 'limit']
        if not isinstance(book, str) and not len(book):
            raise ApiClientError({'message': 'book not specified'})
        if not isinstance(side, str) and side not in _sides:
            raise ApiClientError({'message': 'side not specified'})
        if not isinstance(type, str) and type not in _types:
            raise ApiClientError({'message': 'type not specified'})
        if not str(kwargs.get('major','')).strip() and not str(kwargs.get('minor','')).strip():
            raise ApiClientError({'message': 'an order must be specified in terms of major or minor, never both'})
        if str(kwargs.get('price')).strip() and not (type == 'limit'):
            raise ApiClientError({'message': 'price for use only with limit orders'})
        url = '%s/orders/' % self.base_url
        parameters = {}
        parameters['book'] = book
        parameters['type'] = type
        parameters['side'] = side
        if 'major' in kwargs:
            parameters['major'] = kwargs.get('major')
        if 'minor' in kwargs:
            parameters['minor'] = kwargs.get('minor')
        if 'price' in kwargs:
            parameters['price'] = kwargs.get('price')
        resp = self._request_url(url, 'POST', params=parameters, private=True)
        return resp['payload']

    def funding_destination(self, fund_currency):
        raise NotImplementedError

    def btc_withdrawal(self, amount, address):
        raise NotImplementedError

    def eth_withdrawal(self, amount, address):
        raise NotImplementedError

    def spei_withdrawal(self):
        raise NotImplementedError

