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
from io import BytesIO
from pony.orm import db_session
from telebot import TeleBot
from .config import TELEBOT, TELE_USER_DB, DEBUG
from .qrdecode import qr_decode
from . import Loader


bot = TeleBot(TELEBOT)


def add_receipt(fn, fd, fs, db):
    Loader.load_schemas()
    seller = Loader.get_database(db)[0]
    with db_session:
        try:
            return seller.add_sale(fn, fd, fs)
        except Exception as e:
            if DEBUG:
                print(e)
            return str(e)


@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    username = message.chat.username
    if username not in TELE_USER_DB:
        msg = 'Access denied'
    else:
        try:
            fn, fd, fs = message.text.split()
            db = TELE_USER_DB[username]
            msg = add_receipt(fn, fd, fs, db)
        except ValueError:
            msg = 'NEED space separated list of FN FD FS'

    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['photo'])
def image_process(message):
    username = message.chat.username
    if username not in TELE_USER_DB:
        msg = 'Access denied'
    else:
        file_id = message.photo[-1].file_id
        file_obj = bot.get_file(file_id)
        file_bin = bot.download_file(file_obj.file_path)
        decoded = qr_decode(BytesIO(file_bin))
        if decoded:
            db = TELE_USER_DB[username]
            msg = add_receipt(db=db, **decoded)
        else:
            msg = 'QR invalid'

    bot.send_message(message.chat.id, msg)
