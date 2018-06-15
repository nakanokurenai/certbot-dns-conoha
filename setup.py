from setuptools import setup
from setuptools import find_packages


setup(
    name='certbot-dns-conoha',
    author="nakanokurenai",
    author_email='master@yukarium.net',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certbot',
        'zope.interface',
        'urllib3',
        'six',
        'certifi'
    ],
    entry_points={
        'certbot.plugins': [
            'dns-conoha = certbot_dns_conoha:Authenticator'
        ]
    },
)
