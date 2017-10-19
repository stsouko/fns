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
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from importlib.util import find_spec
from ..config import DB_DATA_LIST
from ..version import version
from .main_create import create_core
from .main_add import add_core


def _add(subparsers):
    parser = subparsers.add_parser('add', help='This utility add data',
                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--fn', '-n', type=int, help='FN')
    parser.add_argument('--fd', '-d', type=int, help='FD')
    parser.add_argument('--fs', '-s', type=int, help='FS')
    parser.add_argument("--database", '-db', type=str, default=DB_DATA_LIST[0], choices=DB_DATA_LIST,
                        help='Database name for addition')
    parser.set_defaults(func=add_core)


def _create_db(subparsers):
    parser = subparsers.add_parser('create', help='This utility create new db',
                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--name', '-n', help='schema name', required=True)
    parser.add_argument('--user', '-u', type=str, help='admin login')
    parser.add_argument('--pass', '-p', type=str, help='admin pass')
    parser.set_defaults(func=create_core)


def argparser():
    parser = ArgumentParser(description='FNS', epilog="(c) Dr. Ramil Nugmanov", prog='fns')
    parser.add_argument("--version", "-v", action="version", version=version(), default=False)
    subparsers = parser.add_subparsers(title='subcommands', description='available utilities')

    _create_db(subparsers)
    _add(subparsers)

    if find_spec('argcomplete'):
        from argcomplete import autocomplete
        autocomplete(parser)

    return parser
