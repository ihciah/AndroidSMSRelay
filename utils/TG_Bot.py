# -*- coding: utf-8 -*-

import requests
from config import TG_TOKEN, USE_PROXY, PROXY, CHAT_ID

__author__ = 'ihciah'


class TGBot:
    @staticmethod
    def send_message(text, user=0):
        tg_message_url = "https://api.telegram.org/bot%s/sendMessage" % TG_TOKEN
        user = int(user)
        data = {"chat_id": CHAT_ID[user] if user < len(CHAT_ID) else user,
                "text": text,
                "disable_notification": False
                }
        res = requests.post(tg_message_url, data, proxies=PROXY).json()
        if res["ok"]:
            return res["result"]["message_id"]
        return None

    @staticmethod
    def send_image(image_url, caption="", user=0):
        tg_photo_url = "https://api.telegram.org/bot%s/sendPhoto" % TG_TOKEN
        user = int(user)
        data = {"chat_id": CHAT_ID[user] if user < len(CHAT_ID) else user,
                "photo": image_url,
                "disable_notification": False,
                }
        if caption:
            data["caption"] = caption
        requests.post(tg_photo_url, data, proxies=PROXY)

    @staticmethod
    def update_message(text, message_id, user=0):
        tg_update_url = "https://api.telegram.org/bot%s/editMessageText" % TG_TOKEN
        user = int(user)
        data = {"chat_id": CHAT_ID[user] if user < len(CHAT_ID) else user,
                "text": text,
                "message_id": message_id
                }
        requests.post(tg_update_url, data, proxies=PROXY)
