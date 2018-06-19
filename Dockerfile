FROM certbot/certbot

COPY . src/certbot-dns-conoha

RUN pip install --no-cache-dir src/certbot-dns-conoha
