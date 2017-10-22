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
from datetime import datetime
from decimal import Decimal
from pony.orm import PrimaryKey, Required, Set, composite_key
from requests import get
from .config import (DEBUG, FNS_SERVER, PROTO_VERSION, CLIENT_VERSION, DEVICE_OS, DEVICE_ID, USER_AGENT,
                     USER_LOGIN, USER_PASSWORD)


def load_tables(db, schema):
    class Seller(db.Entity):
        _table_ = '%s_seller' % schema if DEBUG else (schema, 'seller')
        id = PrimaryKey(int, auto=True)
        title = Required(str)
        inn = Required(str, unique=True)
        sales = Set('Sale')

        @classmethod
        def add_sale(cls, fn, fd, fs):
            fn, fd, fs = fn.lstrip('0'), fd.lstrip('0'), fs.lstrip('0')
            if FiscalNumber.exists(sign=fs, drive=fn, document=fd):
                raise Exception('Receipt exists')

            url = '%s/v1/inns/*/kkts/*/fss/%s/tickets/%s' % (FNS_SERVER, fn, fd)
            q = get(url, params={'fiscalSign': fs, 'sendToEmail': 'no'}, auth=(USER_LOGIN, USER_PASSWORD),
                    headers={'ClientVersion': CLIENT_VERSION, 'Version': PROTO_VERSION, 'Device-OS': DEVICE_OS,
                             'Device-Id': DEVICE_ID, 'User-Agent': USER_AGENT})

            if q.status_code != 200:
                raise Exception('Error: %s' % q.text)

            data = q.json()['document']['receipt']
            date = datetime.strptime(data['dateTime'], '%Y-%m-%dT%H:%M:%S')
            user = data['user'] or 'No Name'
            inn = data['userInn']
            if not data['items']:
                raise Exception('Empty receipt')

            items = {}
            for x in data['items']:
                key = (x['name'], Decimal(x['price'] / 100))
                if key in items:
                    q, s = items[key]
                    items[key] = (q + x['quantity'], s + Decimal(x['sum'] / 100))
                else:
                    items[key] = (x['quantity'], Decimal(x['sum'] / 100))

            seller = cls.get(inn=inn) or cls(title=user, inn=inn)
            fiscal = FiscalNumber(sign=fs, drive=fn, document=fd, date=date)
            for (name, price), (quantity, _sum) in items.items():
                Sale(seller=seller, title=name, price=price, quantity=quantity, sum=_sum, fiscal=fiscal)

            return Decimal(data['totalSum'] / 100)

    class Sale(db.Entity):
        _table_ = '%s_sale' % schema if DEBUG else (schema, 'sale')
        id = PrimaryKey(int, auto=True)
        title = Required(str)
        price = Required(Decimal, precision=10, scale=2)
        quantity = Required(float)
        sum = Required(Decimal, precision=12, scale=2)
        seller = Required('Seller')
        fiscal = Required('FiscalNumber')

    class FiscalNumber(db.Entity):
        _table_ = '%s_fiscal' % schema if DEBUG else (schema, 'fiscal')
        id = PrimaryKey(int, auto=True)
        sign = Required(str)
        drive = Required(str)
        document = Required(str)
        date = Required(datetime)
        composite_key(sign, drive, document)
        sales = Set('Sale')

    return Seller, Sale
