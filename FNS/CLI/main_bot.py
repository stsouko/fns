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
from requests.exceptions import ReadTimeout, ConnectionError
from telebot.apihelper import ApiException
from time import sleep
from ..telebot import bot


def bot_core(**kwargs):
    while True:
        try:
            bot.polling(none_stop=kwargs['non_stop'])
        except (ReadTimeout, ConnectionError, ApiException) as e:
            print(e)
            if kwargs['non_stop']:
                sleep(10)
                print('restarting')
                continue

        break
