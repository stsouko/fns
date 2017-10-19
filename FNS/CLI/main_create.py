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
from pony.orm import Database, sql_debug
from ..config import DEBUG, DB_PASS, DB_HOST, DB_USER, DB_NAME
from ..models import load_tables


def create_core(**kwargs):
    schema = kwargs['name']
    user = DB_USER if kwargs['user'] is None else kwargs['user']
    password = DB_PASS if kwargs['pass'] is None else kwargs['pass']

    x = Database()
    load_tables(x, schema)

    if DEBUG:
        sql_debug(True)
        x.bind('sqlite', 'database.sqlite')
    else:
        x.bind('postgres', user=user, password=password, host=DB_HOST, database=DB_NAME)

    x.generate_mapping(create_tables=True)
