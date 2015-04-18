import csv
import dataserv


def list_to_file(targ_list):
    with open('inv_list','a+') as tempfile:
        for i in range(0, len(targ_list)):
            tempfile.write(repr(targ_list[i]))
            tempfile.write(",")
            tempfile.write("\n")

def extend_list(targ_list):
    idinv_list = []
    for i in targ_list:
        idinv_list.extend(i['Id'])

def recurs_iter(target):
    if type(target) is list:
        src = recurs_iter(iter(target))

    return type(src)

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

def padlist(list1, list2):
    if len(list1)>len(list2):
        padding=(len(list1)-len(list2))*[0]
        list2.extend(padding)
    elif len(list2)>len(list1):
        padding=(len(list2-len(list1))*[0])
        list1.extend(padding)
    else:
        print("Didn't work, give me only 2 lists please")

    ziplist = zip(list1, list2)

    return ziplist

def better_datecompare(date1,date2):
    from datetime import datetime, timedelta
    date1=date1.timetuple()
    date2=date2.timetuple()
    date1=datetime(date1.tm_year,date1.tm_mon,date1.tm_mday)
    date2=datetime(date2.tm_year,date2.tm_mon,date2.tm_mday)
    days=date2-date1

    return days

def convert_infusiondate(IS_dateobject):
    from datetime import datetime
    date = IS_dateobject.timetuple()
    date = datetime(date.tm_year, date.tm_mon, date.tm_mday)

    return date

def linecount(filename):
    if type(filename) != str:
        filename = str(filename)

    with open(filename) as file:
        for i, l in enumerate(file):
            pass

        return i + 1

def leadtime_test():
    import dataserv as ds
    limit=dict(limit=1000)
    lts=ds.LeadtimetoSale().leadtime(**limit)
    ds.Process().procarray(lts)
    for item in lts:
        print(item)

def leadtime_test2():
    import dataserv as ds
    id_pages = ds.Query()._getpages('Contact','Id')
    limit = 999
    lts = []
    for page in range(0, id_pages + 1):
        ref_point = dict(page = page, limit = limit)
        lts.extend(ds.LeadtimetoSale().leadtime(**ref_point))
    ds.Process().procarray(lts)
    for item in lts:
        print(item)
