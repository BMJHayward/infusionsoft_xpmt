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


def datefromcsv(file):
    reader = csv.DictReader(file, delimiter=';')         #read the csv file
    for row in reader:
        date = datetime.strptime(row['Order Date'], '%Y-%m-%d %H:%M:%S')     #datetime value in the right date format
        values[date.strftime('%Y-%m-%d')] += 1          #increment the date with a step of 1

    for date, value in sorted(values.items()):
        result = (value / 3927.2) * 100          #Sla calcul with the theoritic number of line
        print('Date: {}'.format(date))        #SLA display
        print('Result: {}'.format(result))


def monthToNum(date):
    return{
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }[date]


def numToMonth(num):
    return{
        1 : 'Jan',
        2 : 'Feb',
        3 : 'Mar',
        4 : 'Apr',
        5 : 'May',
        6 : 'Jun',
        7 : 'Jul',
        8 : 'Aug',
        9 : 'Sep',
        10 : 'Oct',
        11 : 'Nov',
        12 : 'Dec',
    }[num]


class SQLtoPandas:
    ''' Basic SQL tasks in pandas DataFrames. '''

    self.describe = self.df.describe()

    '''SELECT * FROM <table> LIMIT 10'''
    self.df[:10]
    '''SELECT col1, col2, FROM <table> LIMIT 3'''
    self.df[[col1, col2]][:3]
    '''SELECT col1, col2, col3 FROM <table> ORDER BY col3 LIMIT 3'''
    self.df.sort(col3)[[col1, col2, col3]][:3]
    '''SELECT col1, col2, col3 FROM <table> ORDER BY col3 desc LIMIT 3'''
    self.df.sort(col3, ascending=False)[[col1, col2, col3]][:3]
    '''SELECT * FROM <table> WHERE col1='somevalue' or col1='someother'
       ORDER BY col2 desc LIMIT 5;'''
    self.df[(df[col1]=='somevalue' | (df[col1]=='someother')].sort(col2, ascending=False)[:5]
    '''SELECT * FROM <table> WHERE col1 < 9000
       ORDER BY col3 DESC LIMIT 1;'''
    self.df[df[col1]<9000].sort(col3, ascending=False)[:1]
    '''SELECT COUNT(DISTINCT(col1)) FROM <table>;'''
    len(self.df(col1).unique())
    '''SELECT DISTINCT(col1) FROM
       (SELECT * FROM <table> ORDER BY col2 DESC LIMIT 20);'''
    self.df[:20].sort(col2, ascending=False)[col1].unique()
    '''SELECT col1, COUNT(col1) AS alt_col1_name FROM
       (SELECT * FROM col2 ORDER BY col3 LIMIT 100)
       GROUP BY col1 ORDER BY alt_col1_name DESC;'''
    self.df[:100][col1].value_counts()
    '''SELECT col1, AVG(col2), AVG(col3) FROM
       (SELECT * FROM <table> ORDER BY col3 DESC LIMIT 100)
       GROUP BY col1;'''
    self.df.sort(col3)[:100].groupby(col1).mean()[[col2, col3]]
    '''SELECT col1, COUNT(col1) FROM <table> GROUP BY col1;'''
    self.df.groupby(col1).count()[table]
    '''SELECT * FROM <table1> LEFT JOIN <table2>
       ON <table1>.col1=<table2>.col1 LIMIT 1;'''
    self.df1 = pd.read_csv('df1.csv')
    self.df2 = pd.read_csv('df2.csv')
    self.df1.merge(self.df2, on=col1)[:1]

    def __init__(*csvfiles):
        import pandas as pd
        self.df_array = []
        for csvfile in csvfile:
            self.df = pd.read_csv(csvfile)
            self.df.head()
            self.df_array.append(self.df)
        return self.df_array


if __name__ == "__main__":
    x = linecount()
    print(x)
