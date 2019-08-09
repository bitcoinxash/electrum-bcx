#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

import os
import sys
import platform
import importlib.util
import argparse
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install

MIN_PYTHON_VERSION = "3.6.1"
_min_python_version_tuple = tuple(map(int, (MIN_PYTHON_VERSION.split("."))))


if sys.version_info[:3] < _min_python_version_tuple:
    sys.exit("Error: Electrum requires Python version >= %s..." %
             MIN_PYTHON_VERSION)

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

# load version.py; needlessly complicated alternative to "imp.load_source":
version_spec = importlib.util.spec_from_file_location(
    'version', 'electrum_bcx/version.py')
version_module = version = importlib.util.module_from_spec(version_spec)
version_spec.loader.exec_module(version_module)

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path',
                        metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-bcx.desktop']),
        (os.path.join(usr_share, icons_dirname), [
         'electrum_bcx/gui/icons/electrum.png']),
    ]

extras_require = {
    'hardware': requirements_hw,
    'fast': ['pycryptodomex', 'quark_hash'],
    'gui': ['pyqt5'],
}
extras_require['full'] = [pkg for sublist in list(
    extras_require.values()) for pkg in sublist]


setup(
    name="Electrum-bcx",
    version=version.ELECTRUM_VERSION,
    python_requires='>={}'.format(MIN_PYTHON_VERSION),
    install_requires=requirements,
    extras_require=extras_require,
    packages=[
        'electrum_bcx',
        'electrum_bcx.gui',
        'electrum_bcx.gui.qt',
        'electrum_bcx.plugins',
    ] + [('electrum_bcx.plugins.'+pkg) for pkg in find_packages('electrum_bcx/plugins')],
    package_dir={
        'electrum_bcx': 'electrum_bcx'
    },
    package_data={
        '': ['*.txt', '*.json', '*.ttf', '*.otf'],
        'electrum_bcx': [
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ],
        'electrum.gui': [
            'icons/*',
        ],
    },
    scripts=['electrum_bcx/electrum-bcx'],
    data_files=data_files,
    description="Lightweight bcx Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://electrum.bitcoinxash.com",
    long_description="""Lightweight bcx Wallet""",
)
