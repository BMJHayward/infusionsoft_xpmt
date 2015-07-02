'''
using matplotlib to viz dates.txt
'''
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as pltdates
import pandas as pd
import sqlite3
import dataserv

def getdatesfromfile():
    datefile = input('please enter datefile name: ')
    dates = eval(open(datefile,'r+').read())
    datescount = Counter(dates)
    datescount[20080627] = 500

def matplot_bar(datescount):
    labels, values = zip(*datescount.items())

    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

def pandas_histogram(dates):
    datesdf = pd.DataFrame(dates)
    plt.figure()
    datesdf.plot(kind='bar', alpha=0.5)
    plt.show()

def plotdates(datelist, valuelist):
    yerp=dataserv.Leadtime()
    newdatelist = []
    for i in datelist:
        if not isinstance(i, str):
            i=i[0]
        j = yerp.convert_datestring(i)
        newdatelist.append(j)
    dates = pltdates.date2num(newdatelist)
    plt.plot_date(dates, valuelist)

def sqltopandas():
    db = input('please enter DB name: ')
    sqlquery = input('please enter SQL query to execute: ')
    with sqlite3.connect(db) as con:
        dbquery = pd.read_sql(sqlquery, con)

    return dbquery
