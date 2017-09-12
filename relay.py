# -*- coding: utf-8 -*-

import os
import sqlite3
import requests
import datetime
import time
from contact_book import Contact
from config import TG_TOKEN, MEM_SAVE_PATH, SAVE_PATH, LAST_FILE, PROXY, CHAT_ID, FREE_SIZE, CHECK_INTERVAL, CONTACT

__author__ = 'ihciah'

last_time = 0
contact_book = Contact(CONTACT)

def get_file_path():
    statvfs = os.statvfs('/dev/shm')
    free = statvfs.f_frsize * statvfs.f_bavail / 1024 / 1024
    return MEM_SAVE_PATH if free > FREE_SIZE else SAVE_PATH


def clean_env():
    to_delete = ['/dev/shm/mmssms.db', '/dev/shm/mmssms.db-journal',
                 '/tmp/mmssms.db', '/tmp/mmssms.db-journal']
    for f in to_delete:
        if os.path.exists(f):
            os.remove(f)


def send_telegram(address, date, date_sent, body):
    message = u"%s\n\nRecv at %s\nSend at %s\n\nSender: %s(%s)"
    date, date_sent = [datetime.datetime.fromtimestamp(int(d) / 1000).strftime('%m-%d %H:%M:%S')
                       for d in (date, date_sent)]
    ret, sender_name = contact_book.num2name(address)
    if not ret:
        sender_name = "No matching contact"
    data = {"chat_id": CHAT_ID,
            "text": message % (body, date, date_sent, address, sender_name),
            "disable_notification": False
            }
    TG_IMAGE_URL = "https://api.telegram.org/bot%s/sendMessage" % TG_TOKEN
    requests.post(TG_IMAGE_URL, data, proxies=PROXY)


def get_last_time():
    if not os.path.isfile(LAST_FILE):
        return int(time.time() * 1000)
    with open(LAST_FILE) as f:
        last = f.read().strip()
    if last.isdigit() and len(last) > 9:
        return int(last)
    return int(time.time() * 1000)


def save_last_time(t):
    global last_time
    last_time = t
    with open(LAST_FILE, "w") as fw:
        fw.write(str(t))


def read_and_update_db():
    global last_time
    db_path = get_file_path()
    last_time = get_last_time() if last_time == 0 else last_time
    DOWNLOAD_COMMAND = "/usr/bin/adb pull /data/data/com.android.providers.telephony/databases/mmssms.db %s"
    os.system(DOWNLOAD_COMMAND % db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    SQL = 'SELECT _id,address,date,date_sent,body FROM sms WHERE date>%d AND type=1 ORDER BY date ASC'
    cursor.execute(SQL % last_time)
    values = cursor.fetchall()
    print values
    for _id, address, date, date_sent, body in values:
        send_telegram(address, date, date_sent, body)
        save_last_time(date)
    conn.close()
    clean_env()

if __name__ == "__main__":
    while True:
        try:
            read_and_update_db()
        except:
            pass
        time.sleep(CHECK_INTERVAL)


