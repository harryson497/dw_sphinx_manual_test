#!/usr/bin/env python
# encoding: utf-8
"""
@author: HanYunsong
@contact: yshan@aibee.com
@time: 2021/10/18 7:20 下午
@desc: test2
"""

import os
csv = []
tbl = []
dir = "./source/table/Mall-停车场/"
for a,b,c in os.walk(dir):
    if a == dir :
        csv=c
for i in csv:
    if('csv' not in i):
        csv.remove(i)

for i in csv:
    file =  open(f'{dir}{i}','r', encoding='utf-8')
    a= file.read()
    tbl.extend(a.split('\n')[1:])

for i in tbl:
    if i != '':
        tc = i.split(',')
        print(f"alter table {tc[0]} set tblproperties('comment' = '{tc[1]}')")
