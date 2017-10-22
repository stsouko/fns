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
from pyzbar.pyzbar import decode
from PIL import Image


replace = {'fn': 'fn', 'fp': 'fs', 'i': 'fd'}


def qr_decode(img):
    for x in decode(Image.open(img)):
        if x.type == 'QRCODE':
            try:
                data = {}
                for y in x.data.decode().split('&'):
                    k, v = y.split('=')
                    if k in replace:
                        data[replace[k]] = v.strip()
                if len(data) == 3:
                    return data
            except ValueError:
                pass
