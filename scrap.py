import glob
import os, os.path
import sys
import csv
import dataserv
import statistics
import sqlite3
from datetime import date
import time


# this is straigh out of the docs for cmd module:
def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

def histogram():
    '''
    using bokeh to visualise:
    >>> from bokeh.plotting import figure, output_file, show
    >>> output_file('histogram.html')
    >>> p = figure(title = 'insert title')
    >>> x = datescount.keys()
    >>> y = datescount.values()
    >>> p.line(x,y)
    >>> show(p)
    '''

    dates = eval(open('dates.txt', 'r+').read())
    from collections import Counter
    datescount = Counter(dates)

    return datescount

def sourcelist(cxn):
    testlist = [cxn.dates(), cxn.tags(), cxn.leadsources()]

    return testlist

def filelinecount(filename):
    if type(filename) != str:
        filename = str(filename)

    with open(filename) as file:
        for i, l in enumerate(file):
            pass

        return i + 1

def linecount():
    numlines = []
    for file in list(os.walk('.'))[0][2]:
        if file.endswith('py'):
            try:
                numlines.append(filelinecount(file))
            except: pass

    return sum(numlines)

def quickdbtest():
    salesdata = dataserv.LocalDB().get_csv('sales.csv')
    try:
        dataserv.LocalDB().sendto_sqlite(salesdata, 'sales', db='salesdatatest.sqlite')
    except sqlite3.OperationalError as e:
        print('Please delete table and try again:\n', e, e.__class__, sys.exc_info()[2])

def datestringtotuple(datestring):
    datstr = datestring.split('/')
    datstr = ''.join(datstr)
    datstr = time.strptime(datstr, '%d%m%Y')
    return datstr


if __name__ == "__main__":
    x = linecount()
    print(x)
