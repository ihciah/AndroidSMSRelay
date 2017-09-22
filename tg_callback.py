# -*- coding: utf-8 -*-

from flask import Flask, request

from config import KB_COMMAND, KB_IMAGE_CAPTION, FIND_CONTACT_COMMAND, SMS_COMMAND
from config import TG_TOKEN, KB_IMAGE, CHAT_ID, CONTACT
from utils.TG_Bot import TGBot
from utils.contact_book import Contact
from utils.misc import FileLock
from utils.sms import send_sms

__author__ = 'ihciah'

contact = Contact(CONTACT)

app = Flask(__name__)


def parse_authorized_message(message):
    if 'text' not in message:
        return
    original_text = message['text'].strip()
    card = CHAT_ID.index(message['chat']['id'])

    # Send sms
    text = original_text.split(" ", 2)
    if len(text) >= 3 and text[0] in SMS_COMMAND:
        send_sms(text[1], text[2], card)
        return True

    # Lookup contact
    text = original_text.split(" ", 1)
    if len(text) == 2 and text[0] in FIND_CONTACT_COMMAND:
        contact.send_contact(text[1], card)
        return True

    # KB command
    text = original_text
    if text in KB_COMMAND:
        TGBot.send_image(KB_IMAGE, KB_IMAGE_CAPTION)
        return True

    return False


def parse_normal_message(message):
    if 'text' not in message:
        return
    chat_id = message['chat']['id']

    # Reply chat ID
    if message['text'] == "id":
        TGBot.send_message(str(chat_id), chat_id)
    else:
        TGBot.send_message("Command not found:\n%s" % message['text'], chat_id)


def handle_message(msg):
    message = msg['message']
    flag = False
    if message['chat']['id'] in CHAT_ID:
        FileLock.wait_lock()
        try:
            FileLock.create_lock()
            flag = parse_authorized_message(message)
        finally:
            FileLock.delete_lock()
    if not flag:
        parse_normal_message(message)


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

