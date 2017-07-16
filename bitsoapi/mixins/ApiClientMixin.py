import hashlib
import hmac
import json
import requests
import time
from urlparse import urlparse
from urllib import urlencode


def current_milli_time():
    nonce = str(int(round(time.time() * 1000000)))
    return nonce


class ApiClientMixin:

    def _request_url(self, url, verb, params=None, private=False):
        headers = None
        if params == None:
            params = {}
        if private:
            headers = self._build_auth_header(verb, url, json.dumps(params))
        if verb == 'GET':
            url = self._build_url(url, params)
            if private:
                headers = self._build_auth_header(verb, url)
            try:
                resp = requests.get(url, headers=headers)
            except requests.RequestException as e:
                raise
        elif verb == 'POST':
            try:
                resp = requests.post(url, json=params, headers=headers)
            except requests.RequestException as e:
                raise
        elif verb == 'DELETE':
            try:
                resp = requests.delete(url, headers=headers)
            except requests.RequestException as e:
                raise
        data = self._parse_json(resp.content.decode('utf-8'))
        return data

    def _build_auth_header(self, http_method, url, json_payload=''):
        if json_payload == {} or json_payload == '{}':
            json_payload = ''
        url_components = urlparse(url)
        request_path = url_components.path
        if url_components.query != '':
            request_path += '?' + url_components.query
        nonce = current_milli_time()
        msg_concat = nonce + http_method.upper() + request_path + json_payload
        signature = hmac.new(
            self._secret.encode('utf-8'),
            msg_concat.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return {'Authorization': 'Bitso %s:%s:%s' % (self.key, nonce, signature)}

    def _build_url(self, url, params):
        if params and len(params) > 0:
            url = url + '?' + self._encode_parameters(params)
        return url

    def _encode_parameters(self, parameters):
        if parameters is None:
            return None
        else:
            param_tuples = []
            for k, v in parameters.items():
                if v is None:
                    continue
                if isinstance(v, (list, tuple)):
                    for single_v in v:
                        param_tuples.append((k, single_v))
                else:
                    param_tuples.append((k, v))
            return urlencode(param_tuples)

    def _parse_json(self, json_data):
        try:
            data = json.loads(json_data)
            self._check_for_api_error(data)
        except:
            raise
        return data

    def _check_for_api_error(self, data):
        if data['success'] != True:
            raise ApiError(data['error'])
        if 'error' in data:
            raise ApiError(data['error'])
        if isinstance(data, (list, tuple)) and len(data) > 0:
            if 'error' in data[0]:
                raise ApiError(data[0]['error'])

