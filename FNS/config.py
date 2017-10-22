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
from pathlib import Path
from os.path import expanduser  # python 3.4 ad-hoc
from sys import stderr
from traceback import format_exc

FNS_SERVER = 'https://proverkacheka.nalog.ru:9999'
CLIENT_VERSION = '1.4.1.3'
PROTO_VERSION = '2'
DEVICE_OS = 'Adnroid 4.4.4'
USER_AGENT = 'okhttp/3.0.1'

DEVICE_ID = None
USER_LOGIN = None
USER_PASSWORD = None

TELEBOT = None
TELE_USER_DB_MAP = None

DEBUG = True

DB_USER = None
DB_PASS = None
DB_HOST = None
DB_NAME = None
DB_DATA = None


config_list = ('DB_USER', 'DB_PASS', 'DB_HOST', 'DB_NAME', 'DB_DATA', 'DEVICE_OS', 'DEVICE_ID', 'USER_AGENT',
               'PROTO_VERSION', 'CLIENT_VERSION', 'FNS_SERVER', 'USER_LOGIN', 'USER_PASSWORD', 'TELEBOT',
               'TELE_USER_DB_MAP')

config_load_list = ['DEBUG']
config_load_list.extend(config_list)

config_dirs = [x / '.FNS.ini' for x in (Path(__file__).parent, Path(expanduser('~')), Path('/etc'))]

if not any(x.exists() for x in config_dirs):
    with config_dirs[1].open('w') as f:
        f.write('\n'.join('%s = %s' % (x, y or '') for x, y in globals().items() if x in config_list))

with next(x for x in config_dirs if x.exists()).open() as f:
    for n, line in enumerate(f, start=1):
        try:
            line = line.strip()
            if line and not line.startswith('#'):
                k, v = line.split('=')
                k = k.rstrip()
                v = v.lstrip()
                if k in config_load_list:
                    globals()[k] = int(v) if v.isdigit() and k != 'USER_PASSWORD' else \
                        v == 'True' if v in ('True', 'False', '') else v
        except ValueError:
            print('line %d\n\n%s\n consist errors: %s' % (n, line, format_exc()), file=stderr)

DB_DATA_LIST = DB_DATA.split() if DB_DATA else []

if TELE_USER_DB_MAP:
    tmp = TELE_USER_DB_MAP.split()
    if len(tmp) > 1:
        TELE_USER_DB = {x: y for x, y in zip(tmp[::2], tmp[1::2]) if y in DB_DATA_LIST}
    else:
        TELE_USER_DB = {}
else:
    TELE_USER_DB = {}
