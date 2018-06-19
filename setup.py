from setuptools import setup
from setuptools import find_packages

setup(
    name='certbot-dns-conoha',
    version='0.1.0',
    description='ConoHa DNS Authenticator plugin for certbot.',
    url='https://github.com/nakanokurenai/certbot-dns-conoha',
    author='nakanokurenai',
    author_email='master@yukarium.net',
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha', 'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux', 'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP', 'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration', 'Topic :: Utilities', ),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certbot', 'zope.interface', 'urllib3', 'six', 'certifi'
    ],
    entry_points={
        'certbot.plugins': ['dns-conoha = certbot_dns_conoha:Authenticator']
    }, )
