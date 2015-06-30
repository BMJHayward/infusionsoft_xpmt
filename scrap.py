import glob
import os, os.path
import sys
import csv
import dataserv
import statistics
import sqlite3
from datetime import date
import time

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

def get_db_column(dbname, dbtbl, dbcol):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute('SELECT {0} FROM {1}'.format(dbcol, dbtbl))
    returncolumn = cur.fetchall()
    return returncolumn

def plotdates(datelist, valuelist):
    from matplotlib import pyplot as plt  # probably want this in separate file to dataserv when ready
    from matplotlib import dates as pltdates
    yerp=dataserv.Leadtime()
    newdatelist = []
    for i in datelist:
        if not isinstance(i, str):
            i=i[0]
        j = yerp.convert_datestring(i)
        newdatelist.append(j)
    dates = pltdates.date2num(newdatelist)
    plt.plot_date(dates, valuelist)

if __name__ == "__main__":
    x = linecount()
    print(x)
