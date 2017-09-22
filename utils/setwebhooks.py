# -*- coding: utf-8 -*-
# Script to set telegram webhooks

import requests
from config import PROXY, TG_TOKEN

__author__ = 'ihciah'

DOMAIN = "https://ihc.im/"

url = "https://api.telegram.org/bot%s/setWebhook" % TG_TOKEN
res = requests.post(url, {"url": "%s%s" % (DOMAIN, TG_TOKEN)}, proxies=PROXY)
print res.content
