# -*- coding: utf-8 -*-

import re
import json

__author__ = 'ihciah'

person_patten = re.compile(r'BEGIN:VCARD(.*?)END:VCARD', re.DOTALL)
fullname_patten = re.compile(r'FN:(.*?)\n')
mobile_patten = re.compile(r':\+*?(\d{9}\d*?)\n')

f = open(r'data/iCloud vCard-wyh.vcf')
fc = f.read()
people = person_patten.findall(fc)
f.close()

names = {}
for p in people:
    for i in fullname_patten.findall(p):
        name = i
    if len(name.strip()) == 0:
        continue
    p = p.replace("-", "")
    for i in mobile_patten.findall(p):
        if len(i) == 13 and i[:2] == "86":
            i = i[2:]
        names[i] = name

fl = open("dump", "w")
fl.write(json.dumps(names))
fl.close()
