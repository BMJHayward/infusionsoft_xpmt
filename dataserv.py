'''
=========================
Infusionsoft Experiment
=========================


[![Build Status](https://travis-ci.org/BMJHayward/infusionsoft_xpmt.svg?branch=master)](https://travis-ci.org/BMJHayward/infusionsoft_xpmt)

API wrapper for Infusionsoft CRM. Infusionsoft a.k.a. 'IS' from here on. Intended usespecific reporting not found in

For target reports see classes inheriting from LocalDB, Query and Extract in dataserv.py.

DESCRIPTION
=============

Extract, transform, load data from IS, send to excel, csv, pandas, matplotlib, numpy etc.
This project will keep to the stdlib where ever possible to minimise dependencies, simplify deployment in several environme


dataserv.py is the main file of interest for the moment. this may be broken up in futuremore classes are ad

TODO:
========

+ Update tests - remove duplication
+ Remove hardcoded database names, e.g. dataserv.db
    + 7 places: 117, 142, 165, 358, 498, 560, 578
+ use pandas or matplotlib for dataviz
+ base method for common statistics
+ base method to return dict of common statistics
+ base method to connect to DB, do query, fetchall(), return and close DB
+ DONE: possible Report() class for inidividual reports to inherit from
+ DONE: complete methods to compare datetime objects
+ DONE: LeadtimeToSale() to output useful table of date(1stpurchase-1stcontact)
+ DONE: create file of functions to call _basequery() with different args
+ DONE:refactor CostSaleLeadource to return table-like object with column names as headers
'''
import glob
import os
import sqlite3
import csv
import time
import statistics
from datetime import datetime, timedelta, date
from infusionsoft.library import Infusionsoft
import json
import locale
import pickle
from collections import OrderedDict


class LocalDB:
    ''' Methods for operating on local sqlite database.
        Would like report classes to be able use either Query or LocalDB in the same way. Maybe.
    '''
    @staticmethod
    def sendto_sqlite(query_array, newtable, db='dataserv.db'):
        '''Use sqlite3 module to output to local DB. Saves API calls. Using text datatypes
        in tables to avoid type conversion for datetime objects.
        '''

        conn = sqlite3.connect(db)
        c = conn.cursor()

        if isinstance(query_array, dict):
            create_table = 'CREATE TABLE ' + newtable + ' (key text, value integer);'
            c.execute(create_table)
            insert_into_table = 'INSERT INTO ' + newtable + ' values (?,?);'
            for item in query_array:
                c.executemany(insert_into_table, item.iteritems())

        elif isinstance(query_array, list):
            create_table = 'CREATE TABLE ' + newtable + str(tuple(query_array.pop(0))) + ' ;'
            c.execute(create_table)
            questionmarks = '('+''.join(['?,' for i in range(len(query_array[0])-1)])+'?)'
            insert_into_table = 'INSERT INTO ' + newtable + ' values ' + questionmarks + ';'
            c.executemany(insert_into_table, query_array)

        else:
            raise TypeError('Need to pass list or dict')

        conn.commit()
        conn.close()

    @staticmethod
    def sendto_json(query_array, filename):
        '''Use json to store entire query as json file.'''

        with open(filename, 'x') as file:
            for item in query_array:
                json.dumps(item, file)

    @staticmethod
    def get_db_table(db_name, db_table):
        # c.execute("SELECT name FROM sqlite_master WHERE type='table';")  # gives you available tables
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM {}'.format(db_table))
        db_tbl = c.fetchall()

        return db_tbl

    @staticmethod
    def get_csv(filename):
        ''' Give local csv file as string, returns a list of lists of that file. '''

        csvdata = []
        with open(filename, newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            csvdata.extend([entry for entry in reader])

        return csvdata

    @staticmethod
    def convert_invoice():
        '''Converts currency column in AUD to float.'''

        locale.setlocale(locale.LC_ALL, '')
        conn = sqlite3.connect('dataserv.db')
        c = conn.cursor()
        c.execute('SELECT [Order Total], rowid from sales;')
        invoices = c.fetchall()

        for row in invoices:
            invoices[invoices.index(row)] = list(row)

        for invoice in invoices:
            invoice[0] = invoice[0].strip('AUD')
            invoice[0] = invoice[0].strip('-AUD')
            invoice[0] = invoice[0].strip('N/')
            try:
                invoice[0] = locale.atof(invoice[0])
            except ValueError:
                invoice[0] = 0  # Because some contacts have orders with no total recorded in IS. Not sure why.

        for row in invoices:
            invoices[invoices.index(row)] = tuple(row)

        c.executemany('UPDATE sales set [Order Total]=? where rowid=?;', invoices)
        conn.commit()
        conn.close()

    @staticmethod
    def create_joinlisttable():
        ''' Creates join of two tables. Currently on uses sales and contacts table.
            Might open this to other tables later.
        '''
        conn = sqlite3.connect('dataserv.db')
        c = conn.cursor()

        join_contacts_invoices = '''\
        SELECT contacts.Id, contacts.[Date Created], contacts.[Lead Source],\
        sales.[Order Total], sales.Date \
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

    @staticmethod
    def get_invoicedates():
        ''' Returns list of purchase dates for each contact. '''
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


class Query:
    '''Create connection to API and run basic queries.'''

    def __init__(self):
        ''' Instantiate Infusionsoft object and create connection to
           account app.
        '''
        self.key = os.environ['INFUSION_APIKEY']
        self.app_name = os.environ['INFUSION_APPNAME']
        self.infusionsoft = Infusionsoft(self.app_name, self.key)

    def _basequery(self, **kwargs):
        '''Query contact table by default. Overwrite search parameters with
            kwargs. Combine with _getpages() to return whole database.
        '''
        self.default = dict(
            table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['City','State','Country']
            )

        if kwargs is not None:
            self.default.update(kwargs)

        try:
            self.data = self.infusionsoft.DataService(
                'query', self.default['table'],
                self.default['limit'], self.default['page'],
                self.default['queryData'], self.default['returnData']
                )

            return self.data

        except Exception as exc:
            print('Error running query: ', exc)

    def _count(self, table, field):
        '''Return number of entries in table to retrieve all data.
            Return an int to use as limit in queries, append to list results.
        '''
        self.count = self.infusionsoft.DataService('count', table, {field: '%'})

        return self.count

    def _getpages(self, table, field):
        '''Calculate number of pages to search through using dataservice.'''
        self.totalrecords = self._count(table, field)
        self.pages = (self.totalrecords//999 + 1)

        return self.pages


class Extract(Query):
    '''Pull mass data for analysis using Query() as base. Intended as layer
      between direct queries and each report class.
    '''
    def __init__(self):
        '''Use super() to create API connection.
        Timeframes for reported data.'''
        self.thirtydays = None
        self.month = None
        self.quarter = None
        self.year = None
        self.alltime = None
        super(Extract, self).__init__()

    def tags(self, **kwargs):
        '''Return tags for target contact.'''
        self.tagargs = dict(
            table='ContactGroupAssign',
            queryData={'ContactId': '154084'},
            returnData=['GroupId']
            )

        if kwargs is not None:
                    self.tagargs.update(kwargs)

        self.tag = self._basequery(**self.tagargs)

        return self.tag

    def dates(self, **kwargs):
        '''Return list of date created for all contact types.'''
        self.dateargs = dict(
            table='Contact',
            queryData={'ContactType': '%'},
            returnData=['DateCreated']
            )

        if kwargs is not None:
                    self.dateargs.update(kwargs)

        self.date = self._basequery(**self.dateargs)

        return self.date

    def leadsources(self, **kwargs):
        '''Return leadsource for contacts. Number of contacts is limit key.'''
        self.sourceargs = dict(
            table='Contact',
            queryData={'ContactType': '%'},
            returnData=['Leadsource']
            )

        if kwargs is not None:
                    self.sourceargs.update(kwargs)

        self.leadsource = self._basequery(**self.sourceargs)

        return self.leadsource

    def invoices(self, target_id=None, **kwargs):
        ''' Returns list of dicts, key is 'DateCreated'.
           USAGE:Iterate over list from contact_idanddate() to get target_id.
        '''

        if type(target_id) is str:
            pass
        elif (target_id is not None and type(target_id) is int):
            target_id = str(target_id)
        else:
            print("Input on invoices() failed, check target_id")

        self.inv_args = dict(
            table='Invoice',
            queryData={'ContactId': target_id},
            returnData=['DateCreated']
            )

        if kwargs is not None:
                    self.inv_args.update(kwargs)

        self.inv_dates = self._basequery(**self.inv_args)

        return self.inv_dates

class Leadtime(LocalDB):
    '''
    Use local database to calculate leadtime instead of API.
    Just call stats_leadtime(), returns dict with everything.
    '''


    def stats_LT(self, INCLUDE_LIST = False):
        ''' Main entry point for database form of Leadtime class.
           Pass it nothing, get back dictionary mean, median, quintile and
           std deviation. Component functions listed below in order of appearance.
        '''
        lt = self.get_leadtime()
        average_leadtime = statistics.mean(lt)
        std_dev = statistics.pstdev(lt)
        quintile_5 = int(0.8 * len(lt))
        eightypercentofsales = lt[quintile_5]
        median_leadtime = statistics.median(lt)

        if INCLUDE_LIST == True:
            stats = dict(average_leadtime = average_leadtime,
                standard_deviation = std_dev,
                eightypercent = eightypercentofsales,
                median = median_leadtime,
                fulllist = lt)
        else:
            stats = dict(average_leadtime = average_leadtime,
                standard_deviation = std_dev,
                eightypercent = eightypercentofsales,
                median = median_leadtime)

        return stats

    def get_leadtime(self):
        leadtime = [row['leadtime'] for row in self.get_data().values()]
        leadtime = [i for i in leadtime if i >= 0]

        return leadtime


    def get_data(self):
        data = self.get_db_table('dataserv.db', 'contactsales')
        data = self.list_convert(data)
        data = self.leadtime_from_db(data)

        return data

    def list_convert(self, targetlist):
        newlist = [list(row) for row in targetlist]
        for newrow in newlist:
            newrow[1] = self.convert_datestring(newrow[1])
            newrow[4] = self.convert_datestring(newrow[4])

        return newlist


    def leadtime_from_db(self, targetlist):
        newlist = dict()
        for row in targetlist:
            if row[0] not in newlist.keys():
                newlist[row[0]] = dict(entrydate = row[1], invdates = [row[4]])
            else:
                newlist[row[0]]['invdates'].append(row[4])

            leadtime = min(newlist[row[0]]['invdates']) - newlist[row[0]]['entrydate']
            newlist[row[0]]['leadtime'] = leadtime.days

        return newlist


    def convert_datestring(self, targetdate):

        newdate = targetdate.split()[0]
        newdate = newdate.split('/')
        newdate = [int(n) for n in newdate]
        newdate.reverse()
        newdate = date(newdate[0], newdate[1], newdate[2])

        return newdate

class LeadtimetoSale(Extract):
    '''
    Return length of time from gaining a lead to making first sale.
    HOW TO USE:
    >>> leadtime = LeadtimetoSale().leadtime()
    >>> Output().ascsvdict(leadtime)
    '''
    def leadtime(self, **kwargs):
        ''' Use extract() to get data, use process() to make it sensible.
           Return an object useful for visualistion.
        '''
        self.idd = self.iddates(**kwargs)

        for i in self.idd:
            idarg = i['Id']
            i['Invoices'] = (self.get_inv(idarg))
            self.first_inv_date(i)
            self.get_daystosale(i)

        return self.idd

    def iddates(self, **kwargs):
        '''Returns Id and DateCreated from Contact table as dict.'''
        self.id = dict(returnData = ['Id', 'DateCreated'])
        if kwargs is not None:
            self.id.update(kwargs)

        return self._basequery(**self.id)

    def get_inv(self, idarg):
        '''Returns DateCreated of invoices of id arg.'''
        self.xinf=self.invoices(target_id = idarg)

        return self.xinf

    def first_inv_date(self, dct):
        '''Pass in dict with Invoices key, returns earliest invoice date.'''
        if 'Invoices' in dct.keys():
            inv_dates = dct['Invoices']
            for date in range(0, len(inv_dates)):
                inv_dates[date] = inv_dates[date]['DateCreated']

            if len(inv_dates) == 0:
                first_sale = 0
            elif len(inv_dates) != 0:
                first_sale = min(inv_dates)

            dct['FirstSale'] = first_sale

        else:
            print("Need to give me a dictionary with an 'Invoices' key.")

    def created_minus_sale(self, dct):
        '''Gives number of days between date of lead and date of sale.'''
        leadtime = dct['FirstSale'] - dct['DateCreated']
        dct['LeadTime'] = leadtime

    def get_daystosale(self, leadtimedict):
        '''Pass in dict from LeadtimetoSale(), returns number of days from
        lead generation to first purchase for that contact.
        '''
        if 'DateCreated' and 'FirstSale' in leadtimedict.keys():
            self.created = leadtimedict['DateCreated']
            self.firstsale = leadtimedict['FirstSale']
            self.days = self.datecompare(self.created, self.firstsale)
            leadtimedict['LeadTime'] = self.days
        else:
            print('Need to know FirstSale to do this.')

    def datecompare(self, xmlrpcDateCreated, xmlrpcFirstSale):
        '''Calc days between 2 dates returned from IS.
        Dates passed in must be xmlrpc.client.DateTime if python3.x or
        xmlrpclib.DateTime if python2.x. Can also use DateTime-like
        objects which have the timetuple() method.
        '''

        # need to handle int values of 0 for dates here
        self.date1 = xmlrpcDateCreated.timetuple()
        if type(xmlrpcFirstSale) != int:
            self.date2 = xmlrpcFirstSale.timetuple()
            self.days = time.mktime(self.date2) - time.mktime(self.date1)
            seconds_per_day = 60*60*24
            self.days = self.days // seconds_per_day
        else:
            self.days = 999999  # create outlier to filter or review

        return self.days


class CostSaleLeadsource(LocalDB):
    '''Return a cost per sale per leadsource dictionary.'''
    def stats_CSL(self):

        '''
        +get expenses per leadsource via API
        +get number of sales per leadsource via API
        +combine the two
        ^OR^
        +run leadsource ROI report
        '''
        self.leadsource_ROI = self.get_db_table('dataserv.db', 'leadsource_ROI')
        CSL = OrderedDict()
        CSL['Leadsource'] = ('Percent profit', 'Dollar profit', 'Revenue', 'Expenses')

        for entry in self.leadsource_ROI:
            entry = list(entry)
            self.destring_leadsourceROI_table(entry)
            self.leadsrc = entry[2]
            self.leadsrc_stats = self.ROI_stats(entry)
            CSL[self.leadsrc] = self.leadsrc_stats

        return CSL

    def destring_leadsourceROI_table(self, row):
        ''' Might want to use named constants in to_float and to_int, but
        I will probably only use this here and nowhere else.
        '''
        to_float = {4,5,6,8,10,13,14}  # Uses set because I hardly ever use them and they are cool
        to_int = {0,1,7,9,12}  # I also like looking at them

        for x in to_float:
            try:
                row[x] = float(row[x])
            except:
                row[x] = 0

        for y in to_int:
            try:
                row[y] = int(row[y])
            except:
                row[y] = 0

    def ROI_stats(self, leadsource_row):
        ''' Used to create a dict of dicts with stats for each leadsource. '''
        try:
            expns = leadsource_row[4]
            revnu = leadsource_row[5]
            percent_profit = (1 - (expns / revnu)) * 100
            if hasattr(percent_profit, 'index'):
                percent_profit = percent_profit[0]
        except ZeroDivisionError:
            percent_profit = 0

        dollar_profit  = leadsource_row[5] - leadsource_row[4]
        revenue        = leadsource_row[5]
        expenses       = leadsource_row[4]

        stat_list = [percent_profit, dollar_profit, revenue, expenses]

        return stat_list


class AverageTransactionValue:
    '''Return average amount of transaction across all products.
    TODO: segment by time period, leadsource, product etc.
    +Wouldn't mind breaking this down for each leadsource
    '''
    def stats_ATV(self):
        '''
        +get all sales
        +get number of sales
        +do arithmetic mean
        + e.g: in SQL: SELECT AVG([Order Total]) FROM sales;
        '''

        conn = sqlite3.connect('dataserv.db')
        c = conn.cursor()
        c.execute('SELECT [Order Total] FROM sales;')
        atv = c.fetchall()
        atv = [float(i[0]) for i in atv]
        atv = statistics.mean(atv)
        atv = {'ATV': atv}  # output as dict for same formatting as other report classes
        conn.close()

        return atv

class CustomerLifetimeValue(LocalDB):
    '''Calculate how much any given customer spends on average long term.'''

    def __init__(self):
        SQL_QUERY = 'SELECT ContactId, SUM([Order Total]), [Lead Source] FROM sales \
             GROUP BY ContactId \
             ORDER BY ContactId;'
        conn = sqlite3.connect('dataserv.db')
        c = conn.cursor()

        c.execute(SQL_QUERY)
        CLV_DATA = c.fetchall()
        self.spend = [row[1] for row in CLV_DATA]

        conn.close()

    def stats_CLV(self):
        '''
        +get target contact invoices
        +sum value of all invoices
        +repeat for all contacts who have purchased
        +get average of all contacts lifetimevalue
        +wouldn't mind breaking down CLV by leadsource
        '''
        average_CLV = statistics.mean(self.spend)
        median_CLV = statistics.median(self.spend)
        mode_CLV = statistics.mode(self.spend)
        std_dev = statistics.pstdev(self.spend)
        quintile_5 = int(0.8 * len(self.spend))
        eighty_percent = self.spend[quintile_5]

        stats = dict(average_CLV = average_CLV,
                            standard_deviation = std_dev,
                            eightypercent = eighty_percent,
                            median = median_CLV,
                            mode = mode_CLV)

        return stats


class Process:
    '''Raw query data processed here for target output.
    This class is really only useful when subclassing Extract.
    Kept here for reference for now.
    '''
    def procarray(self, array):
        for dictionary in range(0, len(array)):

            if type(array[dictionary]) is list:
                self.procarray(array[dictionary])

            elif type(array[dictionary]) is dict:
                self.procdict(array[dictionary])

    def procdict(self, dictionary):
        for key in dictionary.keys():

            if key == 'DateCreated':
                self.procdate(key, dictionary)

            elif key == 'FirstSale' and type(dictionary[key]) != int:
                self.procdate(key,dictionary)

            elif key == 'Invoices':
                # self.procarray(dictionary[key])
                invlist = dictionary[key]
                for inv in range(0,len(invlist)):
                    invlist[inv] = self.convert_date(invlist[inv])
                dictionary[key] = invlist
            else:
                pass

    def procdate(self, key, dictionary):
        IS_date = dictionary[key]
        newdate = self.convert_date(IS_date)
        dictionary[key] = newdate

    def convert_date(self, IS_dateobject):
        try:
            convdate = IS_dateobject.timetuple()
            convdate = datetime(convdate.tm_year, convdate.tm_mon, convdate.tm_mday)

            return convdate
        except TypeError as te:
            print("wrong type ", te)

    def combine_list(self, *lists):
        ziplist = zip(*lists)
        ziplist = list(ziplist)

        return ziplist


class Output:
    '''Take data ready for output. Methods to write to file.'''
    @staticmethod
    def stats_outputall():
        allstats = Output().stats_getall()
        for report in allstats:
            Output().ascsv([allstats[report]], report + '.csv')

            print("Report: ", report, " saved to file successfully.")
        Output().strap_csvfiles()

    @staticmethod
    def strap_csvfiles():
        try:
            import xlwt
        except ImportError:
            print('Python installation needs xlwt library. Try pip install xlwt on the command line.')

        wb = xlwt.Workbook()
        reportfiles = ['ATV.csv', 'LT.csv', 'CLV.csv', 'CSL.csv']
        # for filename in glob.glob('*.csv'):  #  TODO: change this to report fies LT,CLV,CSL,ATV
        for filename in reportfiles:
            (f_path, f_name) = os.path.split(filename)
            (f_short_name, f_extension) = os.path.splitext(f_name)
            ws = wb.add_sheet(f_short_name)
            spamReader = csv.reader(open(filename, 'r'))

            for rowx, row in enumerate(spamReader):
                for colx, value in enumerate(row):
                    ws.write(rowx, colx, value)
        wb.save('allstats.xls')

        print('All done! Your file is named \"allstats.xls\".')

    @staticmethod
    def stats_getall():
        ''' Get return data from all report classes,
        return dict of reportname:data pairs.
        '''
        allstats = {
            'LT': Leadtime().stats_LT(),
            'CSL': CostSaleLeadsource().stats_CSL(),
            'ATV': AverageTransactionValue().stats_ATV(),
            'CLV': CustomerLifetimeValue().stats_CLV()
            }

        return allstats

    @staticmethod
    def asfile(target=None, query=None, filename='dataserv.csv'):
        ''' primarily to send to spreadsheet. TODO: use csv module '''

        data = None
        if target is not None:
            data = target
        elif query is not None:
            data = query
        else:
            msg = "No data to output"
            return msg

        with open(filename, 'a+') as tempfile:
            try:
                for line in data:
                    tempfile.write(repr(line))
                    tempfile.write(",")
                    tempfile.write("\n")
                    print(line)
            except TypeError:
                tempfile.write(data)

    @staticmethod
    def ascsv(targlist, outfile):
        '''
        Pass in result of query as list of dicts from query. Alternately, use
        elif to pass result objects in different forms to the one function,
        or to several similar functions contained in Output class.
        '''
        with open(outfile, 'w', newline='') as datafile:
            writer = csv.writer(datafile)
            for item in targlist:
                for key, value in item.items():
                    writer.writerow([key, value])

    @staticmethod
    def ascsvdict(item, outfile):
        '''Item arg is list of dicts. Like ascsv but with DictWriter class.'''
        names = item[0].keys()

        with open(outfile,'w', newline='') as data:
            writer = csv.DictWriter(data, fieldnames=names)
            writer.writeheader()
            writer.writerows(item)

    @staticmethod
    def datetime_to_excel(dateobj):
        xldate = dateobj.strftime('%x')

        return xldate

    @staticmethod
    def ashtml(self, queryfunc, filename):
        '''Put in data, intended to save as valid static webpage.'''
        pass

    @staticmethod
    def asimage(self, queryfunc, filename):
        '''If you just want the visual form of your data.'''
        pass

    @staticmethod
    def as3rdparty(self, queryfunc, filename):
        '''' to send to pandas, matplotlib, etc etc '''
        pass

    @staticmethod
    def to_picklejar(data_to_save, name):
        '''Give whatever object you have to pickle, save it for your next session with given name.'''

        if type(name) != str:
            name = str(name)
        with open(name, 'wb') as picklejar:
            pickle.dump(data_to_save, picklejar)

def importer():
    ''' csvarray should be string including .csv extension in local folder '''
    dbname = input('please enter database name: ')
    datafiles = make_tablename()
    importer = LocalDB()

    for table, filename in datafiles.items():
        tblname = table
        tbldata = importer.get_csv(filename)
        new_headerrow = tbldata[0]
        remove_duplicates(new_headerrow)
        tbldata[0] = new_headerrow

        importer.sendto_sqlite(tbldata, tblname, db=dbname)

    return dbname

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
    '''takes user input at command line for csv files exported from IS'''
    filetypes = {'contacts': '', 'sales': '', 'products': ''}

    for filetype in filetypes.keys():
        filetypes[filetype] = input('please enter filename for {0} data: '.format(filetype))
        if not os.path.isfile(filetypes[filetype]):
            raise FileNotFoundError('File not in this directory. Please check and rerun the program.')

    return filetypes

def main():
    dbname = importer()
    # Output.stats_outputall(db=dbname)

if __name__ == "__main__":
    main()
