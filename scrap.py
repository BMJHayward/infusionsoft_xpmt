import glob
import os, os.path
import sys
import csv
import dataserv
import matplotchart as mpc
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

def plottest():
    import matplotchart as mpc
    import matplotlib.pyplot as plt
    import pandas as pd
    qdata = mpc.sqltopandas()
    dates, values = qdata['Order Date'], qdata['Order Total']
    mpc.plotdates(dates, values)

def column2datetype(db, table, column):
    dateconvert = dataserv.Leadtime()
    conn=sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c=conn.cursor()

    newcolumn = 'py_' + column.strip('[]')
    if ' ' in newcolumn:
        newcolumn = newcolumn.replace(' ','_')
    alterstmt = 'ALTER table {0} ADD COLUMN {1} TEXT'.format(table, newcolumn)
    c.execute(alterstmt)

    querystmt = 'SELECT rowid, {0} FROM {1};'.format(column, table)
    c.execute(querystmt)
    doi = c.fetchall()
    doi = [list(i) for i in doi]

    for date in doi:
        newdate = dateconvert.convert_datestring(date[1])
        newdate = newdate.isoformat()
        c.execute('UPDATE {0} SET {1} = {2} WHERE rowid={3};'.format(table, newcolumn, newdate, date[0]))
    conn.commit()
    conn.close()

def db_updatestrdates(db, table, column):
    datedelta = dataserv.Leadtime()
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT rowid, {0} FROM {1};'.format(column, table))
    datelist = cur.fetchall()
    for dat in datelist:
        newdate = datedelta.convert_datestring(dat[1])
        isodate = newdate.isoformat()


if __name__ == "__main__":
    x = linecount()
    print(x)
