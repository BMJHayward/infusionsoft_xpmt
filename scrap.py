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
    xmlrpclib.DateTime if python2.x.
    '''
    import time
    date1 = xmlrpcFirstSale.timetuple()
    date2 = xmlrpcDateCreated.timetuple()
    days = time.mktime(date1) - time.mktime(date2)

    return days
