"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/brmmm3/fastlogging
"""

import os
import sys
# To use a consistent encoding
from codecs import open
from os import path, listdir

from setuptools import find_packages
try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

BASEDIR = os.path.dirname(__file__)

# Get the long description from the README file
with open(os.path.join(BASEDIR, 'README.rst'), encoding='utf-8') as F:
    long_description = F.read()



setup(
    name='fastlogging',
    version='0.6.0',
    description='An efficient and leightweight logging module.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    url='https://github.com/brmmm3/fastlogging',
    download_url = 'https://github.com/brmmm3/fastlogging/releases/download/0.6.0/fastlogging-0.6.0.tar.gz',

    author='Martin Bammer',
    author_email='mrbm74@gmail.com',
    license='MIT',

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='fast logging',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)

