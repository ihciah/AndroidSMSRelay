# -*- coding: utf-8 -*-

import os
import json
from utils.TG_Bot import TGBot

__author__ = 'ihciah'


class Contact:
    def __init__(self, path="data/dump"):
        self.book = {}
        if os.path.isfile(path):
            with open(path) as f:
                try:
                    d = json.loads(f.read())
                except:
                    d = {}
                self.book = d
        self.rd = dict([(v.replace(" ", ""), k) for k, v in self.book.items()])

    def num2name(self, number):
        number = str(number)
        if len(number) == 13:
            number = number[-11:]
        if number in self.book:
            return True, self.book[number]
        return False, ""

    def search_name(self, name):
        ret = []
        if isinstance(name, (str, unicode)):
            name = [name]
        # if len(name) == 1 and name[0] in self.rd:
        #     ret.append([name, self.rd[name]])
        #     return ret
        for w, num in self.rd.items():
            for word in name:
                if w.find(word) == -1:
                    break
            else:
                ret.append([w, num])
        return ret

    def send_contact(self, names, card):
        result = self.search_name(names.split())
        if result:
            result_message = ("Results for %s:\n" % names) + "\n".join(["%s  %s" % (who, num) for who, num in result])
            TGBot.send_message(result_message, card)
        else:
            TGBot.send_message("No result for %s" % names, card)
