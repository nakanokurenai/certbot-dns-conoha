import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """ConoHa DNS v1 Authenticator Plugin."""

    description = ('ConoHa DNS v1 Authenticator Plugin')

    @classmethod
    def add_parser_arguments(cls, add_argument):
        super(Authenticator, cls).add_parser_arguments(add_argument)
        add_argument('credentials', help='ConoHa credentials INI file.')

    def _setup_credentials(self):
        self.credentials = self._configure_credentials({
            'credentials',
            'ConoHa credentials INI file',
            {
                'dns-endpoint': 'DNS Service endpoint, shown in API Information page',
                'auth-token':   ('Token insert to X-Auth-Token header, get instruction from ',
                                'https://www.conoha.jp/guide/apitokens.php')
            }
        })
