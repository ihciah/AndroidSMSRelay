#! -*- coding: utf-8 -*-

import os
import json

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
        if name in self.rd:
            ret.append([name, self.rd[name]])
        if not ret:
            for w, num in self.rd.items():
                if w.find(name) != -1:
                    ret.append([w, num])
        return ret
