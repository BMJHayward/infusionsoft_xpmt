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
    conn=sqlite3.connect(db)
    c=conn.cursor()
    querystmt = ('SELECT rowid, ? FROM ?;', (column, table))
    # updatestmt = ()
    # alterstmt = ('ALTER table ? ADD COLUMN ? date', (table, column))
    c.execute(querystmt)
    doi = c.fetchall()
    doi = [list(i) for i in doi]
    for date in doi:
        date[1] = dateconvert.convert_datestring(date[1])
        c.execute('UPDATE {0} SET {1} = {2} WHERE rowid={3};'.format(table, column, date[1], date[0]))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    x = linecount()
    print(x)
