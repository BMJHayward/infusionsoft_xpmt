import csv
import dataserv
import statistics
import sqlite3
from datetime import date
import time


def histogram():
    '''
    using bokeh to visualise:
    from bokeh.plotting import figure, output_file, show
    output_file('histogram.html')
    p = figure(title = 'insert title')
    x = datescount.keys()
    y = datescount.values()
    p.line(x,y)
    show(p)
    '''

    dates = eval(open('dates.txt', 'r+').read())
    from collections import Counter
    datescount = Counter(dates)

    return datescount

def sourcelist(cxn):
    testlist = [cxn.dates(), cxn.tags(), cxn.leadsources()]

    return testlist

def linecount(filename):
    if type(filename) != str:
        filename = str(filename)

    with open(filename) as file:
        for i, l in enumerate(file):
            pass

        return i + 1

def destring_leadsourceROI_table(row):
    ''' This probably belongs in class CostSaleLeadsource.
    Might also want to use named constants in to_float and to_int, but
    I will probably only use this here and nowhere else.
    '''
    to_float = {4,5,6,8,10,13,14}  # Uses set because I hardly ever use them and they are cool
    to_int = {0,1,7,9,12}  # I also like looking at them

    for x in to_float:
        row[x] = float(row[x])
    for y in to_int:
        row[y] = int(row[y])
