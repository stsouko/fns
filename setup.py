#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2017 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of FNS.
#
#  FNS is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
from FNS.version import version
from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='FNS',
    version=version(),
    packages=find_packages(),
    url='https://github.com/stsouko/fns',
    license='AGPLv3',
    author='Dr. Ramil Nugmanov',
    author_email='stsouko@live.ru',
    description='FNS',
    entry_points={'console_scripts': ['fns=FNS.CLI:launcher']},
    install_requires=['requests', 'pony', 'pyzbar', 'pillow', 'pytelegrambotapi'],
    extras_require={'postgres_cffi':  ['cffi', 'psycopg2cffi'],
                    'postgres':  ['psycopg2'],
                    'autocomplete': ['argcomplete']},
    long_description=(Path(__file__).parent / 'README.md').open().read(),
    keywords='FNS database',
    classifiers=['Environment :: Web Environment',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 ]
)
