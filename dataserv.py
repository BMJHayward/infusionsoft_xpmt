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
+ composition basic query objects for use in reporting class
+ possible Report() class for inidividual reports to inherit from
+ use pandas or matplotlib for dataviz
+ statistics?
'''

import os
from infusionsoft.library import Infusionsoft


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

class LeadtimeToSale(Extract):
    '''Return length of time from gaining a lead to making first sale.'''
    def leadtime_to_sale(self):
        ''' Use extract() to get data, use process() to make it sensible.
           Return an object useful for visualistion.
        '''

        self.idd=self.iddates()
        self.idd=[list(item.values()) for item in self.idd]

        for element in self.idd:
            self.invlist=self.get_inv(target_id=element[0])
            element.append(self.invlist)

        return self.idd

    def iddates(self, **kwargs):

        self.id = dict(returnData=['Id', 'DateCreated'])

        return self._basequery(**self.id)

    def get_inv(idarg=idarg):

        self.xinf=self.invoices(target_id=idarg)

        return self.xinf

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

    def iter_array(self, array):

        self.data = []
        for dictionary in array:
            if type(dictionary) is list: self.iter_array(dictionary)
            self.data.append(self.query_process(dictionary))

        return self.data


    def query_process(self, dictionary):

        if 'GroupId' in dictionary.keys():

            tag = dictionary['GroupId']

            return tag

        elif 'DateCreated' in dictionary.keys():
            date = str(dictionary['DateCreated'])
            date = date.split('T')[0]
            date = int(date)

            return date

        elif 'Leadsource' in dictionary.keys():

            lead = dictionary['Leadsource']

            return lead

        elif 'Id' in dictionary.keys():

            idnum = dictionary['Id']

            return idnum

        elif 'invoices' in dictionary.keys():

            invlist = self.iter_array(dictionary['invoices'])

            return invlist

    def combine_list(self, *lists):

        ziplist = zip(*lists)
        ziplist = list(ziplist)

        return ziplist


class Output:
    ''' expects target_list to be of type list '''

    def asfile(self, target=None, query=None, filename='dataserv.csv'):
        ''' primarily to send to spreadsheet. TODO: use csv module '''

        self.data = None
        if target is not None:
            self.data = target
        elif query is not None:
            self.data = query
        else:
            msg = "No data to output"
            return msg

        with open(filename, 'a+') as self.tempfile:
            for line in self.data:
                self.tempfile.write(repr(line))
                self.tempfile.write(",")
                self.tempfile.write("\n")
                print(line)

    def asscv(self, queryfunc, filename):

        # import csv
        # with open(filename, newline="") as source:
            # rdr = DictReader(source)
            # data = list(rdr)
            # return data

        raise NotImplementedError

    def ashtml(self, queryfunc, filename):

        raise NotImplementedError


    def asimage(self, queryfunc, filename):

        raise NotImplementedError


    def as3rdparty(self, queryfunc, filename):
        '''' to send to pandas, matplotlib, etc etc '''

        raise NotImplementedError
