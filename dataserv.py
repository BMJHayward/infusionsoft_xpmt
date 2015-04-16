'''
########################
Infusionsoft Experiment
########################

.. image:: https://travis-ci.org/BMJHayward/infusionsoft_xpmt.svg?branch=master
    :target: https://travis-ci.org/BMJHayward/infusionsoft_xpmt

API wrapper for Infusionsoft CRM. Infusionsoft a.k.a. 'IS' from here on. Intended use is specific reporting not found in IS.

For target reports see classes inheriting from Query and Extract in dataserv.py.

DESCRIPTION
############

Extract, transform, load data from IS, send to excel, csv, pandas, matplotlib, numpy etc.
This project will keep to the stdlib where ever possible to minimise dependencies, and simplify deployment in several environments.


dataserv.py is the main file of interest for the moment. this may be broken up in future as more classes are added.

TODO:
######

+ include recordcount() to return all data when using 'all' argument
+ LeadtimeToSale() to output useful table of date(1stpurchase-1stcontact)
+ composition basic query objects for use in reporting class
+ possible Report() class for inidividual reports to inherit from
+ possible Transform() class for things common to each report
+ complete methods to compare datetime objects
+ use pandas or matplotlib for dataviz
+ statistics?
+ create file of functions to call _basequery() with different args
+ tests for class: LeadtimetoSale()
'''

import os
import csv
from datetime import datetime, timedelta
import time
from infusionsoft.library import Infusionsoft
import scrap  # FUTURE TODO: remove this import when ready


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
            # Process().procdict(i)  # Process class should be used last I think
            # self.created_minus_sale(i)

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
            self.days = datecompare(self.created, self.firstsale)
            leadtimedict['LeadTime'] = self.days
        else:
            print('Need to know FirstSale to do this.')

    def datecompare(self, xmlrpcDateCreated, xmlrpcFirstSale):
        '''Calc days between 2 dates returned from IS.
        Dates passed in must be xmlrpc.client.DateTime if python3.x or
        xmlrpclib.DateTime if python2.x. Can also use DateTime-like
        objects which have the timetuple() method.
        '''
        import time
        # need to handle int values of 0 for dates here
        self.date1 = xmlrpcDateCreated.timetuple()
        if type(xmlrpcFirstSale) is not int:
            self.date2 = xmlrpcFirstSale.timetuple()
            self.days = time.mktime(date2) - time.mktime(date1)
            seconds_per_day = 60*60*24
            self.days = self.days // seconds_per_day
        else:
            self.days = 999999  # create outlier to filter or review

        return self.days


class CostSaleLeadsource(Extract):
    '''Return a cost per sale per leadsource object.'''
    def cost_sale_leadsource(self):
        '''
        +get expenses per leadsource
        +get number of sales per leadsource
        +combine the two
        ^OR^
        +run leadsource ROI report
        '''
        raise NotImplementedError


class AvgerageTransactionValue(Extract):
    '''Return average amount of transaction across all products.
    TODO: segment by time period, leadsource, product etc.
    '''
    def average_transaction_value(self):
        '''
        +get all sales
        +get number of sales
        +do arithmetic mean
        '''
        raise NotImplementedError


class CustomerLifetimeValue(Extract):
    '''Calculate how much any given customer spends on average long term.'''
    def customer_lifetime_value(self):
        '''
        +get target contact invoices
        +sum value of all invoices
        +repeat for all contacts who have purchased
        +get average of all contacts lifetimevalue
        '''
        raise NotImplementedError


class Process:
    '''Raw query data processed here for target output.'''
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
            for line in data:
                tempfile.write(repr(line))
                tempfile.write(",")
                tempfile.write("\n")
                print(line)

    @staticmethod
    def ascsv(targlist):
        '''
        Pass in result of query as list of dicts from query. Alternately, use
        elif to pass result objects in different forms to the one function,
        or to several similar functions contained in Output class.
        '''
        with open('dataserv.csv', 'w') as datafile:
            writer=csv.writer(datafile)
            for item in targlist:
                for key, value in item.items():
                    writer.writerow([key, value])

    @staticmethod
    def ascsvdict(item):
        '''Item arg is list of dicts. Like ascsv but with DictWriter class.'''
        names = item[0].keys()
        with open('dataserv.csv','w', newline='') as data:
            writer = csv.DictWriter(data, fieldnames=names)
            writer.writeheader()
            writer.writerows(item)

    @staticmethod
    def datetime_to_excel(dateobj):
        xldate = dateobj.strftime('%x')

        return xldate

    @staticmethod
    def ashtml(self, queryfunc, filename):

        raise NotImplementedError

    @staticmethod
    def asimage(self, queryfunc, filename):

        raise NotImplementedError

    @staticmethod
    def as3rdparty(self, queryfunc, filename):
        '''' to send to pandas, matplotlib, etc etc '''

        raise NotImplementedError
