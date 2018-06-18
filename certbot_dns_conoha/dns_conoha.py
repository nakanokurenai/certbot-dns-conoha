import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common

from conoha_dns_v1 import ConoHaDNSv1 as _ConoHaDNSv1
from threading import Lock

import logging
logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for ConoHa DNS v1."""

    description = ('DNS Authenticator for ConoHa DNS v1')

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self._record_ids = {}
        self._lock = Lock()

    def more_info(self):
        return 'DNS Authenticator for ConoHa DNS v1.'

    @property
    def _client(self):
        return _ConoHaDNSv1(
            endpoint=self.credentials.conf('dns-endpoint'),
            token=self.credentials.conf('auth-token'))

    @classmethod
    def add_parser_arguments(cls, add_argument):
        super(Authenticator, cls).add_parser_arguments(
            add_argument, default_propagation_seconds=5)
        add_argument('credentials', help='ConoHa credentials INI file.')

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials', 'ConoHa credentials INI file', {
                'dns-endpoint':
                'DNS Service endpoint, shown in API Information page',
                'auth-token':
                ('Token insert to X-Auth-Token header, get instruction from '
                 'https://www.conoha.jp/guide/apitokens.php')
            })

    def _perform(self, domain, validation_name, validation):
        domain = self._client.add_record(
            domain_name=domain,
            type='TXT',
            name=validation_name,
            data=validation)
        with self._lock:
            self._record_ids[validation_name + validation] = domain['id']

    def _cleanup(self, domain, validation_name, validation):
        # TODO: get record_id from GET /records API
        with self._lock:
            try:
                record_id = self._record_ids[validation_name + validation]
                self._client.del_record(domain_name=domain, id=record_id)
            except KeyError:
                logger.info('No cleanup required for {} ({}).'.format(validation_name, validation))
