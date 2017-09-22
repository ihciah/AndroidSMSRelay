# -*- coding: utf-8 -*-

TG_TOKEN = "YOUR_TELEGRAM_TOKEN"
CHAT_ID = [259444514, 259444514]  # Your chat id to yourself (2 items for dual sim card)

KB_COMMAND = ["kb", u"课表"]
KB_IMAGE = "https://unknown"
KB_IMAGE_CAPTION = "小海的课表"

FIND_CONTACT_COMMAND = ["search", "contact", "num"]  # Command to query contact book

SMS_COMMAND = ["sms"]  # Command to send sms

# Proxy used when connect telegram
USE_PROXY = True
_PROXY = dict(http='socks5://127.0.0.1:16801', https='socks5://127.0.0.1:16801')
PROXY = None if not USE_PROXY else _PROXY

CONTACT = "/opt/sms/data/dump"  # Path to contact json file
MEM_SAVE_PATH = "/dev/shm/mmssms.db"  # DB saving path when /dev/shm is available
SAVE_PATH = "/tmp/mmssms.db"  # DB saving path when /dev/shm is not available
LAST_FILE = "/opt/sms/data/last"  # File to save the time of last checking

FREE_SIZE = 50
CHECK_INTERVAL = 10
