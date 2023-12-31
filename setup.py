#!/usr/bin/env python
# This file is part of aeb43.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import codecs
import os
import re

from setuptools import find_packages, setup


def read(fname):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), 'r', 'utf-8').read()


def get_version():
    init = read(os.path.join('aeb43', '__init__.py'))
    return re.search("__version__ = '([0-9.]*)'", init).group(1)


setup(name='aeb43',
    version=get_version(),
    description='A module to parse AEB43 files',
    long_description=read('README.rst'),
    author='Tryton',
    author_email='foundation@tryton.org',
    url='https://pypi.org/project/aeb43/',
    download_url='https://downloads.tryton.org/aeb43/',
    project_urls={
        "Bug Tracker": 'https://bugs.tryton.org/aeb43',
        "Forum": 'https://discuss.tryton.org/tags/aeb43',
        "Source Code": 'https://code.tryton.org/aeb43',
        },
    keywords='AEB43 parser',
    packages=find_packages(),
    package_data={
        'aeb43': ['AEB43.txt'],
        },
    python_requires='>=3.8',
    install_requires=['python-stdnum'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        ],
    license='BSD',
    )
