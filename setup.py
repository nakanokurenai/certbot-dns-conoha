from setuptools import setup
from setuptools import find_packages


setup(
    name='certbot_dns_conoha',
    packages=find_packages(),    
    install_requires=[
        'certbot',
        'zope.interface',
    ],
    author="nakanokurenai",
    author_email='master@yukarium.net',
    entry_points={
        'certbot.plugins': [
            'dns_conoha = certbot_dns_conoha:Authenticator'
        ],
    },
)
