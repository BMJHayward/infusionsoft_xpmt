'''
using matplotlib to viz dates.txt
'''
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as pltdates
import pandas as pd

datefile = input('please enter datefile name: ')
dates = eval(open(datefile,'r+').read())
datescount = Counter(dates)
datescount[20080627] = 500
# this value skews the graph too much, original value is approx 23K

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
    datesdf.plot(kind='hist', alpha=0.5)
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
