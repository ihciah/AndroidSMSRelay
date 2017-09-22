# -*- coding: utf-8 -*-
# Script to set telegram webhooks

import requests
from config import PROXY, TG_TOKEN

__author__ = 'ihciah'

CALLBACK = "https://ihc.im/" + TG_TOKEN  # Modify this url to your callback url.

url = "https://api.telegram.org/bot%s/setWebhook" % TG_TOKEN
res = requests.post(url, {"url": CALLBACK}, proxies=PROXY)
print res.content
