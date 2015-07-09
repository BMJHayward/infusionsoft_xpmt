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
    querystmt = ('SELECT ? FROM ?;', (column, table))
    alterstmt = ('ALTER table ? ADD COLUMN ? date', (table, column))
    c.execute(querystmt)
    doi = c.fetchall()
    for date in doi:
        datepoint = dateconvert.convert_datestring(date)


if __name__ == "__main__":
    x = linecount()
    print(x)
