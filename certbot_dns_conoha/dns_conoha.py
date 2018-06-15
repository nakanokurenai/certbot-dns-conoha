import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common

import urllib3
import json
import certifi
from functools import partial
from six.moves.urllib import parse


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for ConoHa DNS v1."""

    description = (
        'DNS Authenticator for ConoHa DNS v1')

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self._record_ids = {}

    def more_info(self):
        return 'hogehuga'

    @property
    def _client(self):
        return _ConoHaDNSv1(
            endpoint=self.credentials.conf('dns-endpoint'),
            token=self.credentials.conf('auth-token')
        )

    @classmethod
    def add_parser_arguments(cls, add_argument):
        super(Authenticator, cls).add_parser_arguments(add_argument, default_propagation_seconds=5)
        add_argument('credentials', help='ConoHa credentials INI file.')

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'ConoHa credentials INI file',
            {
                'dns-endpoint': 'DNS Service endpoint, shown in API Information page',
                'auth-token': (
                    'Token insert to X-Auth-Token header, get instruction from '
                    'https://www.conoha.jp/guide/apitokens.php')
            }
        )

    def _perform(self, domain, validation_name, validation):
        domain = self._client.add_record(domain_name=domain, type='TXT', name=validation_name, data=validation)
        # FIXME: non thread safety
        self._record_ids[validation_name + validation] = domain['id']

    def _cleanup(self, domain, validation_name, validation):
        # FIXME: non thread safety
        # TODO: get record_id from GET /records API
        record_id = self._record_ids[validation_name + validation]
        self._client.del_record(domain_name=domain, id=record_id)


class ZoneNotFoundError(Exception):
    pass


class ConoHaDNSAPIError(Exception):
    pass


class _ConoHaDNSv1():
    def __init__(self, endpoint, token):
        self._endpoint = endpoint
        self._http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        self._token = token

    @staticmethod
    def _to_fqdn(name):
        return name if name[-1] == '.' else name + '.'

    def _request(self, method, url, **kwargs):
        "urllib3.request with context"
        url = parse.urljoin(self._endpoint, url)
        headers = kwargs.pop('headers', {})
        headers['X-Auth-Token'] = self._token
        res = self._http.request(method, url, headers=headers, **kwargs)
        if res.status >= 400:
            raise ConoHaDNSAPIError(res.data)
        return res

    def add_record(self, *_, **kwargs):
        try:
            domain_name = kwargs.get('domain_name', None)
            domain_id = kwargs.get('domain_id', None)
            if domain_name is None and domain_id is None:
                raise ValueError('You must specify "domain_name" or "domain_id".')
            if domain_name is not None and domain_id is not None:
                raise ValueError('You must not specify "domain_name" and "domain_id" at the same time.')
            record_type = kwargs['type']
            record_name = kwargs['name']
            record_data = kwargs['data']
        except KeyError as e:
            raise ValueError(e.message)

        if domain_name and domain_id is None:
            domain_id = self._find_domain_id(name=domain_name)

        data = {
            'name': self._to_fqdn(record_name),
            'type': record_type,
            'data': record_data
        }
        res = self._request(
            'POST',
            '/v1/domains/{id}/records'.format(id=domain_id),
            body=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json'
            }
        )

        return json.loads(res.data.decode('utf-8'))

    def del_record(self, *args, **kwargs):
        try:
            domain_name = kwargs.get('domain_name', None)
            domain_id = kwargs.get('domain_id', None)
            if domain_name is None and domain_id is None:
                raise ValueError('You must specify "domain_name" or "domain_id".')
            if domain_name is not None and domain_id is not None:
                raise ValueError('You must not specify "domain_name" and "domain_id" at the same time.')
            record_id = kwargs['id']
        except KeyError as e:
            raise ValueError(e.message)

        if domain_name and domain_id is None:
            domain_id = self._find_domain_id(name=domain_name)

        self._request(
            'DELETE',
            '/v1/domains/{domain_id}/records/{record_id}'.format(
                domain_id=domain_id,
                record_id=record_id
            )
        )

    def get_domains(self, name=None):
        # name must be FQDN (end with dot)
        url = '/v1/domains'
        if name is not None:
            query = {
                'name': name
            }
            url = '{url}?{query}'.format(url=url, query=parse.urlencode(query))
        res = self._request('GET', url)
        return json.loads(res.data.decode('utf-8'))['domains']

    def _find_domain_id(self, name):
        fqdn = self._to_fqdn(name)
        domains = self.get_domains(fqdn)
        if len(domains) == 0:
            parts = fqdn.split('.')
            if len(parts) == 2:
                raise ZoneNotFoundError
            return self._find_domain_id('.'.join(parts[1:]))
        return domains[0]['id']
