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
    
