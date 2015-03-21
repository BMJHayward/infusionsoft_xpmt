
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

def parse_datetimeobject(dtobj, dataserv):

    '''
    try this later:
    from datetime import datetime
    date_obj = datetime.strptime(dtobj)
    '''
    dtobjframe = dataserv.Process(dtobj)
    dates = dtobjframe.iter_array()
    return dates

def compare_date(date1, date2):

    leadtime = abs(date1 - date2)

    return leadtime
