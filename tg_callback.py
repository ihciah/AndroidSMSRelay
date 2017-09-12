# -*- coding: utf-8 -*-

from flask import Flask, request
import requests
import subprocess
from contact_book import Contact
from config import TG_TOKEN, KB_IMAGE, CHAT_ID, PROXY, CONTACT
from config import KB_COMMAND, KB_IMAGE_CAPTION, FIND_CONTACT_COMMAND, SMS_COMMAND

__author__ = 'ihciah'

contact = Contact(CONTACT)

app = Flask(__name__)


def send_message(text):
    TG_MESSAGE_URL = "https://api.telegram.org/bot%s/sendMessage" % TG_TOKEN
    data = {"chat_id": CHAT_ID,
            "text": text,
            "disable_notification": False
            }
    requests.post(TG_MESSAGE_URL, data, proxies=PROXY)


def send_image(image_url, caption=""):
    TG_PHOTO_URL = "https://api.telegram.org/bot%s/sendPhoto" % TG_TOKEN
    data = {"chat_id": CHAT_ID,
            "photo": image_url,
            "disable_notification": False,
            }
    if caption:
        data["caption"] = caption
    requests.post(TG_PHOTO_URL, data, proxies=PROXY)


def send_sms(message):
    if 'text' not in message:
        return
    text = message['text']
    text = text.split(" ", 2)
    if len(text) >= 3 and text[0] in SMS_COMMAND:
        receiver = text[1].replace("+", "").replace(".", "")
        if not receiver.startswith("86"):
            receiver = "86" + receiver
        if not receiver.isdigit():
            send_message("Number %s is invalid." % text[1])
            return
        sms = text[2]
        sms = sms.replace("\"", "\\\"")
        subprocess.call(['adb', 'shell', 'service', 'call', 'isms', '5', 's16',
                         receiver, 'i32', '0', 'i32', '0', 's16', sms
                         ])
        send_message("SMS to %s has been sent:\n%s" % (receiver, text[2]))
        return
    if len(text) == 2 and text[0] in FIND_CONTACT_COMMAND:
        result = contact.search_name(text[1].strip())
        if result:
            result_message = ("Results for %s:\n" % text[1]) + "\n".join(["%s  %s" % (who, num) for who, num in result])
            send_message(result_message)
        else:
            send_message("No result for %s" % text[1])
        return
    if len(text) == 1 and text[0] in KB_COMMAND:
        send_image(KB_IMAGE, KB_IMAGE_CAPTION)
        return
    send_message("Command not found:\n%s" % message['text'])


def handle_message(msg):
    message = msg['message']
    if message['chat']['id'] == CHAT_ID:
        send_sms(message)


@app.route('/'+TG_TOKEN, methods=['POST'])
def recv():
    j = request.get_json(force=True)
    try:
        handle_message(j)
    except:
        pass
    return "ok", 200

if __name__ == '__main__':
    app.run(host="192.168.102.130", port=11100)

