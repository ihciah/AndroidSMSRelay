# -*- coding: utf-8 -*-
import subprocess
import re

from utils.TG_Bot import TGBot

__author__ = 'ihciah'


def sms_escape(sms):
    sms = sms.replace("\"", "\\\"").replace("\\", "\\\\")
    sms = sms.replace("`", "\\`")
    return sms


def send_sms(number, content, card):
    receiver = str(number).replace("+", "").replace(".", "")
    if receiver[:2] in ["13", "18", "17", "15", "14"] and len(receiver) == 11:
        receiver = "86" + receiver
    if not receiver.isdigit():
        TGBot.send_message("Number %s is invalid." % number, card)
        return
    sms = content
    sms = sms_escape(sms)

    message_id = TGBot.send_message("[Working] Sending message to %s:\n%s" % (receiver, content), card)

    if card == 0:
        # Send message using default sim card
        subprocess.call(['adb', 'shell', 'service', 'call', 'isms', '5', 's16',
                         receiver, 'i32', '0', 'i32', '0', 's16', sms
                         ])
    else:
        # Send message using secondary sim card
        # 61: Tab; 66: Enter; 20: Arrow_Down; 3: Home
        subprocess.call(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO',
                         '-d', 'sms:%s' % receiver, '--es', 'sms_body', '\"%s\"' % sms,
                         '--ez', 'exit_on_sent', 'true', '-S'])
        subprocess.call(['sleep', '3'])
        exec_keycode = [61, 66, 20, 66, 3]
        for key in exec_keycode:
            subprocess.call(['adb', 'shell', 'input', 'keyevent', str(key)])
            subprocess.call(['sleep', '1'])

    if message_id is not None:
        TGBot.update_message("SMS to %s has been sent:\n%s" % (receiver, content), message_id, card)
    else:
        TGBot.send_message("SMS to %s has been sent:\n%s" % (receiver, content), card)


def reply_sms(message_to_reply, sms_content, card):
    if 'text' in message_to_reply:
        reply_text = message_to_reply['text']
        last_line = reply_text.split("\n")[-1]
        pattern = re.compile(r'(\d{3,})')
        m = re.search(pattern, last_line)
        if m:
            send_sms(m.group(0), sms_content, card)
            return
    TGBot.send_message("Cannot reply message!", card)
