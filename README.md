# certbot-dns-conoha
Get certificates by certbot with ConoHa DNS API v1

```sh
curl -X POST -H 'Accept: application/json' -d '{"auth": {"passwordCredentials": {"username": "<username>", "password": "<password>"}, "tenantId": "<tenantId>"}}' https://identity.tyo1.conoha.io/v2.0/tokens -o tokens.json
cat tokens.json | jq '.access.token.id' | xargs -I% echo 'dns_conoha_auth_token = %' >> credentials.ini
cat tokens.json | jq '.access.serviceCatalog | map(select(.type == "dns")) | .[0].endpoints| map(select(.region == "tyo1")) | .[0] | .publicURL' | xargs -I% echo "dns_conoha_dns_endpoint = %" >> credentials.ini
```
