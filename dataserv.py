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
        super(Extract, self).__init__()
        self.thirtydays = None
        self.month = None
        self.quarter = None
        self.year = None
        self.alltime = None

    def tags(self, **kwargs):
        '''Return tags for target contact.'''

        self.tagargs = dict(
            table='ContactGroupAssign',
            limit=10,
            page=0,
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
            limit=10,
            page=0,
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
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['Leadsource']
            )

        if kwargs is not None:
                    self.sourceargs.update(kwargs)

        self.leadsource = self._basequery(**self.sourceargs)

        return self.leadsource

    def contact_idanddate(self, **kwargs):
        '''Return Id AND DateCreated at once for cross-reference later.'''

        self.id_and_date = dict(
            limit=9,
            returnData=['Id','DateCreated']
            )

        if kwargs is not None:
                    self.id_and_date.update(kwargs)

        self.contacts_with_dates = self.dates(**self.id_and_date)

        return self.contacts_with_dates

    def invoices(self, target_id=None, **kwargs):
        '''Iterate over list from contact_idanddatecreated() to get target_id.'''

        if type(target_id) is str:
            pass
        elif (target_id is not None and type(target_id) is int):
            target_id = str(target_id)
        else:
            print("Input on invoices() failed, check target_id")


        self.inv_args = dict(
            table='Invoice',
            limit=9,
            page=0,
            queryData={'ContactId': target_id},
            returnData=['DateCreated']
            )

        if kwargs is not None:
                    self.inv_args.update(kwargs)

        self.inv_dates = self._basequery(**self.inv_args)

        return self.inv_dates



class CostSaleLeadsource(Extract):
    '''Return a cost per sale per leadsource object.'''
    def cost_sale_leadsource(self):

        raise NotImplementedError


class AvgerageTransactionValue(Extract):
    '''Return average amount of transaction across all products.
    TODO: segment by time period, leadsource, product etc.
    '''
    def average_transaction_value(self):

        raise NotImplementedError


class CustomerLifetimeValue(Extract):
    '''Calculate how much any given customer spends on average long term.'''
    def customer_lifetime_value(self):

        raise NotImplementedError


class LeadtimeToSale(Extract):
    ''''Return length of time from gaining a lead to making first sale.
    TODO: Use histograms and other stats to analyse this.
    '''
    def leadtime_to_sale(self):

        raise NotImplementedError


class ContactIdAndDate(Extract):
    '''Return array of contact ids with date created. Most analysis will need
    to cross-reference this data. This should perhaps be in Extract.
    '''

    def contact_invoices(self, id_list=None, inv_list=None):
        ''' combine date from contact_idanddate() and invoices() '''

        if id_list is not None:
            self.iddate_list = self.contact_idanddate(**id_list)
        else:
            self.iddate_list = self.contact_idanddate()

        self.idinv_list = [i['Id'] for i in self.iddate_list]

        self.contact_invlist = []
        for idx in self.idinv_list:
            if inv_list is not None:
                self.yaq = self.invoices(target_id=idx, **inv_list)
            else:
                self.yaq = self.invoices(target_id=idx)

            self.contact_invlist.append([idx, self.yaq])
                # append() keeps Id with invoice date, don't use extend()

        return self.contact_invlist


class Process:
    ''' raw query data processed here for target output'''

    def __init__(self, array):

        self.array = array


    def iter_array(self):

        data = []
        for dictionary in self.array:
            data.append(self.query_process(dictionary))

        return data


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
