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

def parse_datetimeobject(dtobj):
    '''
    try this later:
    from datetime import datetime
    date_obj = datetime.strptime(dtobj)
    '''
    dtobjframe = dataserv.Process(dtobj)
    dates = dtobjframe.iter_array()

    return dates

def earliest_date(datearray):
    earliest = min(datearray)

    return earliest

def compare_date(date1, date2):
    leadtime = abs(date1 - date2)

    return leadtime

def leadtime():
    testcontlist = dataserv.Extract().contact_idanddate()
    testinvlist = dataserv.LeadtimeToSale().contact_invoices()
    '''
        print(parse_datetimeobject(testinvlist[0][1], dataserv)
        print(parse_datetimeobject(testcontlist), dataserv)
    '''
    return [testcontlist,testinvlist]

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

def datecompare(xmlrpcDateCreated, xmlrpcFirstSale):
    '''Calc days between 2 dates returned from IS.
    Dates passed in must be xmlrpc.client.DateTime if python3.x or
    xmlrpclib.DateTime if python2.x. Can also use DateTime-like
    objects which have the timetuple() method.
    '''
    import time
    # need to handle int values of 0 for dates here
    date1 = xmlrpcDateCreated.timetuple()
    if type(xmlrpcFirstSale) is not int:
        date2 = xmlrpcFirstSale.timetuple()
        days = time.mktime(date2) - time.mktime(date1)
        seconds_per_day = 60*60*24
        days = days // seconds_per_day
    else:
        days = 999999  # create outlier to filter or review

    return days

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

def datetime_to_excel(dateobj):
    xldate = dateobj.strftime('%x')

    return xldate

def get_daystosale(leadtimedict):
    '''Pass in dict from LeadtimetoSale(), returns number of days from
    lead generation to first purchase for that contact.
    '''
    if 'DateCreated' and 'FirstSale' in leadtimedict.keys():
        created = leadtimedict['DateCreated']
        firstsale = leadtimedict['FirstSale']
        days = datecompare(created, firstsale)
        leadtimedict['LeadTime'] = days
    else:
        print('Need to know FirstSale to do this.')

def linecount(filename):
    if type(filename) != str:
        filename = str(filename)

    with open(filename) as file:
        for i, l in enumerate(file):
            pass

        return i + 1
