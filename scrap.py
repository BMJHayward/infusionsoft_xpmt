import glob
import os, os.path
import sys
import csv
import dataserv
import matplotchart as mpc
import statistics
import sqlite3
from datetime import date, datetime
import time
from dateutil import parser

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

def datefromcsv():
    reader = csv.DictReader(fil, delimiter=';')         #read the csv file
    for row in reader:
        date = datetime.strptime(row['Order Date'], '%Y-%m-%d %H:%M:%S')     #datetime value in the right date format
        values[date.strftime('%Y-%m-%d')] += 1          #increment the date with a step of 1

    for date, value in sorted(values.items()):
        result = (value / 3927.2) * 100          #Sla calcul with the theoritic number of line
        print 'Date: {}'.format(date)        #SLA display
        print 'Result: {}'.format(result)

def getdatesfromstring(columnname):
    datecolumns = \
        {'Date Created',
        'Last Updated',
        'Program Started date',
        'Assessment Booked Date',
        'Date Sent',
        'Initial Enquiry Date',
        'Date Equipment was received',
        'PlusThis New lead date',
        'Referred date',
        'Order Date',
        'entrydate',
        'invdate'
        }

    if columnname in datecolumns:
        return True


def str2dateconv(datept):
    '''Use to take date columns from db to create datetime objects.'''
    datepoint = parser.parse(datept,dayfirst=True)
    return datepoint

def date2strconv(datept):
    '''Use to write datetime objects back to db in format dd/mm/yyyy.'''
    return datept.strftime('%d/%m/%Y')


if __name__ == "__main__":
    x = linecount()
    print(x)
