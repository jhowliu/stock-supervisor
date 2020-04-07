# -*- coding: utf-8 -*-
#
# Usage: Load all Taiwan stock code info from csv file
#
# TWSE stock = 上市證券
# TPEX stock = 上櫃證券
#

import csv
import os
from collections import namedtuple

ROW = namedtuple('StockCodeInfo', ['type', 'code', 'name', 'ISIN', 'start',
                                   'market', 'group', 'CFI'])
PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TPEX_CSV_PATH = os.path.join(PACKAGE_DIRECTORY, 'tpex_equities.csv')
TWSE_CSV_PATH = os.path.join(PACKAGE_DIRECTORY, 'twse_equities.csv')

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class StockAgents(object, metaclass=Singleton):
    def __init__(self):
        self._codes = {}
        self._tpex = {}
        self._twse = {}
        self.run()

    def run(self):
        if os.path.isfile(TPEX_CSV_PATH):
            self.__read_csv(TPEX_CSV_PATH, 'tpex')

        if os.path.isfile(TWSE_CSV_PATH):
            self.__read_csv(TWSE_CSV_PATH, 'twse')

    def __read_csv(self, path, types):
        with open(path, newline='', encoding='utf_8') as csvfile:
            reader = csv.reader(csvfile)
            csvfile.readline()
            for row in reader:
                row = ROW(*(item.strip() for item in row))
                self._codes[row.code] = row
                if types == 'tpex':
                    self._tpex[row.code] = row
                else:
                    self._twse[row.code] = row

    @property 
    def twse(self):
        return self._twse

    @property
    def tpex(self):
        return self._tpex

    @property
    def codes(self):
        return self._codes
