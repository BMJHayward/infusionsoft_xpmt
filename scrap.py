import glob
import os
import csv
import dataserv
import statistics
import sqlite3
from datetime import date
import time


def importer(dbname, csvarray):
    ''' csvarray should be string including .csv extension in local folder '''
    for csvfile in csvarray:
        importer = dataserv.LocalDB()
        tbldata = importer.get_csv(csvfile)

        tblname = csvfile.split('.')[0]
        new_headerrow = tbldata[0]
        remove_duplicates(new_headerrow)
        tbldata[0] = new_headerrow

        importer.sendto_sqlite(tbldata, tblname, db=dbname)

def remove_duplicates(headerrow):
    ''' Infusionsoft csv files often have duplicate strings as header row.
    When importing to sql, this raises sqlite3.OperationalError. Pass in the
    first row of your csv file to fix this. importer() calls this for you as well.
    '''
    for item in headerrow:  #  this is horrible but works for now
        if headerrow.count(item) > 1:
            idx = headerrow.index(item)
            for col in range(idx + 1, len(headerrow)):
                if headerrow[col] == item:
                    headerrow[col] = '_' + headerrow[col]
            #get index of each occurrence
            #for 2nd occurrence, remove vowels
            #for 3rd, remove vowels, prepend with '_'
            #for more, append with number?
            print(item, ':', headerrow.count(item))

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


if __name__ == "__main__":
    x = linecount()
    print(x)
