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

def sendto_sqlite(query_array):
    '''Use sqlite3 module to output to local DB. Saves API calls. Using text datatypes
    in tables to avoid type conversion for datetime objects.
    '''
    import sqlite3
    conn = sqlite3.connect('dataserv.db')
    c = conn.cursor()
    c.execute('CREATE TABLE contacts (key text, value integer);')
    for item in query_array:
        # insert item into db. think about datatypes here
        # could possibly just write item as one whole string.
        # read it back in as dict later
        c.executemany('insert into contacts values (?,?);', item.iteritems())
    conn.commit()
    conn.close()

def sendto_json(query_array):
    '''Use json to store entire query as json file.'''
    import json
    with open('dataserv.json') as file:
        for item in diclist:
            json.dump(item, file)

def get_csv(filename):
    if type(filename) != str:
        filename = str(filename)
    csvdata = []
    with open(filename, newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        csvdata.extend([entry for entry in reader])
    return csvdata

def convert_invoice():
    '''Converts currency column in AUD to float.'''
    import locale
    import sqlite3
    locale.setlocale(locale.LC_ALL, '')
    conn = sqlite3.connect('dataserv.db')
    c = conn.cursor()
    c.execute('SELECT [Inv Total], rowid from sales;')
    invoices = c.fetchall()
    for row in invoices:
        invoices[invoices.index(row)] = list(row)
    for invoice in invoices:
        invoice[0] = invoice[0].strip('AUD')
        invoice[0] = invoice[0].strip('-AUD')
        invoice[0] = locale.atof(invoice[0])
    for row in invoices:
        invoices[invoices.index(row)] = tuple(row)
    c.executemany('UPDATE sales set [Inv Total]=? where rowid=?;', invoices)
    conn.commit()
    conn.close()

def create_joinlisttable():
    import sqlite3
    
    conn = sqlite3.connect('dataserv.db')
    c = conn.cursor()
    
    join_contacts_invoices = '''\
    SELECT contacts.Id, contacts.[Date Created], contacts.[Lead Source],\
    sales.[Inv Total], sales.Date \
    FROM contacts INNER JOIN sales \
    ON contacts.Id = sales.ContactId;\
    '''
    c.execute(join_contacts_invoices)
    joinlist = c.fetchall()
    joinlist.sort(key = lambda x: x[0])

    c.execute('''CREATE TABLE contactsales(
    contactid text, entrydate text, leadsource text, invamount text, invdate text);''')
    c.executemany('INSERT INTO contactsales VALUES (?,?,?,?,?);', joinlist)
    
    conn.commit()
    conn.close()

def get_invoicedates():
    import sqlite3

    conn = sqlite3.connect('dataserv.db')
    c = conn.cursor()
    conn.text_factory = int
    c.execute('SELECT Id FROM contacts;')
    contact_idlist = c.fetchall()
    contact_invlist = dict()
    conn.text_factory = str
    for cid in contact_idlist:
        c.execute('SELECT Date FROM sales where sales.ContactId = (?);', cid)
        contact_invlist[cid] = c.fetchall()
    conn.close()
    return contact_invlist

def leadtime_fromdb(datecreated, invdates):
    '''
    datecreated: contact creation date
    invdates: list of invoice dates for same contact
    '''

    dt_creat = convert_datestring(datecreated)
    new_invdates = [convert_datestring(date) for date in invdates]
    firstsale = min(new_invdates)
    leadtime = firstsale - dt_creat

    return leadtime  # this will be number of days

def convert_datestring(targetdate):
    import time
    seconds_per_day = 60*60*24
    newdate = time.strptime(targetdate.split()[0], '%d/%m/%Y')
    newdate = time.mktime(newdate)
    newdate = newdate // seconds_per_day

    return newdate

def list_convert(targetlist):
    newlist = [list(row) for row in targetlist]
    for newrow in newlist:
        newrow[1] = convert_datestring(newrow[1])
        newrow[4] = convert_datestring(newrow[4])

    return newlist

def get_db_table(db_name, db_table):
    import sqlite3

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('SELECT * FROM {}'.format(db_table))
    db_tbl = c.fetchall()

    return db_tbl

def leadtime_from_db(targetlist):
    newlist = dict()
    for row in targetlist:
        if row[0] not in newlist.keys():
            newlist[row[0]] = dict(entrydate = row[1], invdates = [row[4]])
        else: 
            newlist[row[0]]['invdates'].append(row[4])
    
        leadtime = min(newlist[row[0]]['invdates']) - newlist[row[0]]['entrydate']
        newlist[row[0]]['leadtime'] = leadtime

    return newlist

def get_data():
    data = get_db_table('dataserv.db', 'contactsales')
    data = list_convert(data)
    data = leadtime_from_db(data)
    
    return data

def get_leadtime():
    leadtime = [row['leadtime'] for row in get_data().values()]

    return leadtime

def stats_leadtime():
    lt = get_leadtime()
    average_leadtime = sum(lt)/len(lt)
    std_dev = statistics.pstdev(lt)
    quintile_5 = 0.8*len(lt)
    eightypercentofsales = lt[quintile_5]
    median_leadtime = statistics.median(lt)

    stats = dict(average_leadtime = average_leadtime,
                standard_deviation = standard_deviation,
                eightypercent = eightypercentofsales,
                median = meadian_leadtime,
                fulllist = lt)

    return stats
