import glob
import os
import csv
import dataserv
import statistics
import sqlite3
from datetime import date
import time
import cmd, sys

class dataservShell(cmd.Cmd):
    '''user interface to do everything in a few steps. PyQt suggested for GUI.
    will keep this as separate branch to come back to later.
    1: user puts in csv files
    2: this class creates DB using dataserv.LocalDB
    3: creates reports for each: ATV, CLV, LTS and CLS
    4: runs Output.stats_getall()
    5: notifies user when finished
    '''
    def importer(dbname, csvarray):
        ''' csvarray should be string including .csv extension in local folder '''
        for csvfile in csvarray:
            importer = dataserv.LocalDB()
            tbldata = importer.get_csv(csvfile)

            tblname = csvfile.split('.')[0]  # replace this with func to return tblname based on what user says the file is
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

                print(item, ':', headerrow.count(item))

    def make_tablename():
        '''choose your file. include the .csv extension'''  # use input() for this?
        '''LocalDB.get_csv(chosen_file)'''
        '''tablename is contacts, sales, products as chosen by user'''
        '''return filename, tablename'''

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

''' DO THIS to run dataservShell:
if __name__ == '__main__':
    dataservShell().cmdloop()
'''
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
