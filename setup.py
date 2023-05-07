#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

NAME = 'rotate-screen'
DESCRIPTION = 'A small Python package for rotating the screen.'
URL = 'https://github.com/danny-burrows/rotate-screen'
EMAIL = 'dannyburrows@protonmail.com'
AUTHOR = 'Danny Burrows'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.1.5'

INSTALL_REQUIRES = [
    "pywin32;platform_system=='Windows'"
]

# Optional package for the examples...
EXTRAS = {
    'shortcuts_example': ['keyboard']
}

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Desktop Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)
