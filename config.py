# -*- coding: utf-8 -*-

TG_TOKEN = "YOUR_TELEGRAM_TOKEN"
CHAT_ID = 259444514  # Your chat id to yourself

KB_COMMAND = ["kb", u"课表"]
KB_IMAGE = "https://unknown"
KB_IMAGE_CAPTION = "小海的课表"

FIND_CONTACT_COMMAND = ["search", "contact", "num"]

SMS_COMMAND = ["sms"]

PROXY = dict(http='socks5://127.0.0.1:16801', https='socks5://127.0.0.1:16801')

CONTACT = "/opt/sms/data/dump"
MEM_SAVE_PATH = "/dev/shm/mmssms.db"
SAVE_PATH = "/tmp/mmssms.db"
LAST_FILE = "/opt/sms/data/last"

FREE_SIZE = 50
CHECK_INTERVAL = 10
