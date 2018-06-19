# certbot-dns-conoha [![][circleci-badge]][circleci] [![PyPI version][pypi-badge]][pypi] [![][docker-hub-build-status-badge]][docker-hub]

Get certificates by certbot with ConoHa DNS API v1

Install
---
```sh
pip install certbot-dns-conoha
```

Usage
---
```sh
certbot -a certbot-dns-conoha:dns-conoha certonly -d example.com --certbot-dns-conoha:dns-conoha-credentials credentials.ini
```

How to generate credentials.ini
---
```sh
curl -X POST -H 'Accept: application/json' -d '{"auth": {"passwordCredentials": {"username": "<username>", "password": "<password>"}, "tenantId": "<tenantId>"}}' https://identity.tyo1.conoha.io/v2.0/tokens -o tokens.json
cat tokens.json | jq '.access.token.id' | xargs -I% echo 'certbot_dns_conoha:dns_conoha_auth_token = %' >> credentials.ini
cat tokens.json | jq '.access.serviceCatalog | map(select(.type == "dns")) | .[0].endpoints| map(select(.region == "tyo1")) | .[0] | .publicURL' | xargs -I% echo "certbot_dns_conoha:dns_conoha_dns_endpoint = %" >> credentials.ini
```

[pypi]: https://pypi.org/project/certbot-dns-conoha/
[pypi-badge]: https://badge.fury.io/py/certbot-dns-conoha.svg
[circleci]: https://circleci.com/gh/nakanokurenai/certbot-dns-conoha/tree/master
[circleci-badge]: https://circleci.com/gh/nakanokurenai/certbot-dns-conoha/tree/master.svg?style=svg
[docker-hub-build-status-badge]: https://img.shields.io/docker/build/nakanokurenai/certbot-dns-conoha.svg
[docker-hub]: https://hub.docker.com/r/nakanokurenai/certbot-dns-conoha/
