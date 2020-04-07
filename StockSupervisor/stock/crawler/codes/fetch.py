# -*- coding: utf-8 -*-
#
# Usage: Download all stock code info from TWSE
#
# TWSE equities = 上市證券
# TPEx equities = 上櫃證券
#

import csv
import os
from collections import namedtuple

import requests
from lxml import etree

from stock.crawler.utils import get_proxies

TWSE_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
TPEX_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
ROW = namedtuple('Row', ['type', 'code', 'name', 'ISIN', 'start',
                         'market', 'group', 'CFI'])


def make_row_tuple(typ, row):
    code, name = row[1].split('\u3000')
    return ROW(typ, code, name, *row[2: -1])


def fetch_data(url):
    r = requests.get(url, proxies=get_proxies())
    root = etree.HTML(r.text)
    trs = root.xpath('//tr')[1:]

    result = []
    typ = ''
    for tr in trs:
        tr = list(map(lambda x: x.text, tr.iter()))
        if len(tr) == 4:
            # This is type
            typ = tr[2].strip(' ')
        else:
            # This is the row data
            result.append(make_row_tuple(typ, tr))
    return result


def to_csv(path, data):
    with open(path, 'w', newline='', encoding='utf_8') as csvfile:
        writer = csv.writer(csvfile,
                            delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data[0]._fields)
        for d in data:
            writer.writerow([_ for _ in d])

def __get_directory():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return dir_name

def update_codes():
    twse_data = fetch_data(TWSE_URL)
    tpex_data = fetch_data(TPEX_URL)

    to_csv(os.path.join(__get_directory(), 'twse_equities.csv'), twse_data)
    to_csv(os.path.join(__get_directory(), 'tpex_equities.csv'), tpex_data)


if __name__ == '__main__':
    twse_data = fetch_data(TWSE_URL)
    tpex_data = fetch_data(TPEX_URL)
    to_csv(os.path.join(__get_directory(), 'twse_equities.csv'), twse_data)
    to_csv(os.path.join(__get_directory(), 'tpex_equities.csv'), tpex_data)
