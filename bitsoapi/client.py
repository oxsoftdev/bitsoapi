from .mixins.ApiClientMixin import ApiClientMixin
from .models import (
    AvailableBooks
    , Ticker
)


class Api(ApiClientMixin):

    def __init__(self, key=None, secret=None):
        self.base_url = 'https://bitso.com/api/v3'
        self.key = key
        self._secret = secret

    # public api

    def available_books(self):
        url = '%s/available_books/' % self.base_url
        resp = self._request_url(url, 'GET')
        return AvailableBooks._NewFromJsonDict(resp)

    def ticker(self, book):
        url = '%s/ticker/' % self.base_url
        parameters = {}
        parameters['book'] = book
        resp = self._request_url(url, 'GET', params=parameters)
        return Ticker._NewFromJsonDict(resp['payload'])

