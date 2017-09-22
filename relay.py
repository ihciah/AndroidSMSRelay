# -*- coding: utf-8 -*-

import datetime
import os
import sqlite3
import time

from config import CHECK_INTERVAL, CONTACT
from utils.TG_Bot import TGBot
from utils.contact_book import Contact
from utils.misc import LastFile, clean_env, get_db_save_path

__author__ = 'ihciah'

contact_book = Contact(CONTACT)
last_time = LastFile()


def send_telegram(address, date, date_sent, body, user=0):
    message = u"%s\n\nRecv at %s\nSend at %s\n\nSender: %s (%s)"
    date, date_sent = [datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%m-%d %H:%M:%S')
                       for d in (date, date_sent)]
    ret, sender_name = contact_book.num2name(address)
    if not ret:
        sender_name = "No matching contact"
    TGBot.send_message(message % (body, date, date_sent, address, sender_name), user)


def read_db():
    db_path = get_db_save_path()
    DOWNLOAD_COMMAND = "/usr/bin/adb pull /data/data/com.android.providers.telephony/databases/mmssms.db %s"
    os.system(DOWNLOAD_COMMAND % db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    SQL = 'SELECT _id,address,date,date_sent,body,sub_id FROM sms WHERE date>%d AND type=1 ORDER BY date ASC'
    cursor.execute(SQL % last_time.get_last_time())
    values = cursor.fetchall()
    print values
    for _id, address, date, date_sent, body, sub_id in values:
        send_telegram(address, date, date_sent, body, sub_id)
        last_time.update_time(date)
    conn.close()
    clean_env()

if __name__ == "__main__":
    while True:
        try:
            read_db()
        finally:
            pass
        time.sleep(CHECK_INTERVAL)
