import glob
import os
import csv
import dataserv
import statistics
import sqlite3
from datetime import date
import time


def importer():
    ''' csvarray should be string including .csv extension in local folder '''
    dbname = input('please enter database name: ')
    datafiles = make_tablename()
    importer = dataserv.LocalDB()
    for table, filename in datafiles:
        tblname = table
        tbldata = importer.get_csv(filename)
        new_headerrow = tbldata[0]
        remove_duplicates(new_headerrow)
        tbldata[0] = new_headerrow

        importer.sendto_sqlite(tbldata, tblname, db=dbname)

def remove_duplicates(headerrow):
    ''' Infusionsoft csv files often have duplicate strings as header row.
    When importing to sql, this raises sqlite3.OperationalError. Pass in the
    first row of your csv file to fix this. importer() calls this for you as well.
    '''
    for item in headerrow:  # this is horrible but works for now
        if headerrow.count(item) > 1:
            idx = headerrow.index(item)
            for col in range(idx + 1, len(headerrow)):
                if headerrow[col] == item:
                    headerrow[col] = '_' + headerrow[col]

            print(item, ':', headerrow.count(item))

def make_tablename():
    '''choose your file. include the .csv extension'''  # use input() for this?
    '''LocalDB.get_csv(chosen_file)'''
    '''tablename is contacts, sales, products as chosen by user'''
    '''return filename, tablename'''
    filetype = None

    filetypes = {'contacts': '', 'sales': '', 'products': ''}

    for filetype in filetypes:
        filetypes[filetype] = input('please enter filename for {0} data: '.format(filetype))

    return filetypes

def test_make_tablename():
    '''this belongs in testfile when done'''
    '''choose file'''
    '''check file exists'''
    '''assert filetype is chosen'''
    '''assert filetype is (sales|contacts|products)'''

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


if __name__ == "__main__":
    x = linecount()
    print(x)
