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

CLASSES:
=========

builtins.object
    Output
    Process
    Query
        Extract
            AvgerageTransactionValue
            CostSaleLeadsource
            CustomerLifetimeValue
            LeadtimetoSale

**class AvgerageTransactionValue(Extract)**
   Return average amount of transaction across all products.
   TODO: segment by time period, leadsource, product etc.

   Method resolution order:
       AvgerageTransactionValue
       Extract
       Query
       builtins.object

   Methods defined here:

   average_transaction_value(self)
       +get all sales
       +get number of sales
       +do arithmetic mean

   ----------------------------------------------------------------------
   Methods inherited from Extract:

   __init__(self)
       Use super() to create API connection.
       Timeframes for reported data.

   dates(self, **kwargs)
       Return list of date created for all contact types.

   invoices(self, target_id=None, **kwargs)
       Returns list of dicts, key is 'DateCreated'.
       USAGE:Iterate over list from contact_idanddate() to get target_id.

   leadsources(self, **kwargs)
       Return leadsource for contacts. Number of contacts is limit key.

   tags(self, **kwargs)
       Return tags for target contact.

   ----------------------------------------------------------------------
   Data descriptors inherited from Query:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class CostSaleLeadsource(Extract)**
   Return a cost per sale per leadsource object.

   Method resolution order:
       CostSaleLeadsource
       Extract
       Query
       builtins.object

   Methods defined here:

   cost_sale_leadsource(self)
       +get expenses per leadsource
       +get number of sales per leadsource
       +combine the two
       ^OR^
       +run leadsource ROI report

   ----------------------------------------------------------------------
   Methods inherited from Extract:

   __init__(self)
       Use super() to create API connection.
       Timeframes for reported data.

   dates(self, **kwargs)
       Return list of date created for all contact types.

   invoices(self, target_id=None, **kwargs)
       Returns list of dicts, key is 'DateCreated'.
       USAGE:Iterate over list from contact_idanddate() to get target_id.

   leadsources(self, **kwargs)
       Return leadsource for contacts. Number of contacts is limit key.

   tags(self, **kwargs)
       Return tags for target contact.

   ----------------------------------------------------------------------
   Data descriptors inherited from Query:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class CustomerLifetimeValue(Extract)**
   Calculate how much any given customer spends on average long term.

   Method resolution order:
       CustomerLifetimeValue
       Extract
       Query
       builtins.object

   Methods defined here:

   customer_lifetime_value(self)
       +get target contact invoices
       +sum value of all invoices
       +repeat for all contacts who have purchased
       +get average of all contacts lifetimevalue

   ----------------------------------------------------------------------
   Methods inherited from Extract:

   __init__(self)
       Use super() to create API connection.
       Timeframes for reported data.

   dates(self, **kwargs)
       Return list of date created for all contact types.

   invoices(self, target_id=None, **kwargs)
       Returns list of dicts, key is 'DateCreated'.
       USAGE:Iterate over list from contact_idanddate() to get target_id.

   leadsources(self, **kwargs)
       Return leadsource for contacts. Number of contacts is limit key.

   tags(self, **kwargs)
       Return tags for target contact.

   ----------------------------------------------------------------------
   Data descriptors inherited from Query:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class Extract(Query)**
   Pull mass data for analysis using Query() as base. Intended as layer
   between direct queries and each report class.

   Method resolution order:
       Extract
       Query
       builtins.object

   Methods defined here:

   __init__(self)
       Use super() to create API connection.
       Timeframes for reported data.

   dates(self, **kwargs)
       Return list of date created for all contact types.

   invoices(self, target_id=None, **kwargs)
       Returns list of dicts, key is 'DateCreated'.
       USAGE:Iterate over list from contact_idanddate() to get target_id.

   leadsources(self, **kwargs)
       Return leadsource for contacts. Number of contacts is limit key.

   tags(self, **kwargs)
       Return tags for target contact.

   ----------------------------------------------------------------------
   Data descriptors inherited from Query:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class LeadtimetoSale(Extract)**
   Return length of time from gaining a lead to making first sale.
   HOW TO USE:
   >>> leadtime = LeadtimetoSale().leadtime()
   >>> Output().ascsvdict(leadtime)

   Method resolution order:
       LeadtimetoSale
       Extract
       Query
       builtins.object

   Methods defined here:

   created_minus_sale(self, dct)
       Gives number of days between date of lead and date of sale.

   first_inv_date(self, dct)
       Pass in dict with Invoices key, returns earliest invoice date.

   get_inv(self, idarg)
       Returns DateCreated of invoices of id arg.

   iddates(self, **kwargs)
       Returns Id and DateCreated from Contact table as dict.

   leadtime(self)
       Use extract() to get data, use process() to make it sensible.
       Return an object useful for visualistion.

   ----------------------------------------------------------------------
   Methods inherited from Extract:

   __init__(self)
       Use super() to create API connection.
       Timeframes for reported data.

   dates(self, **kwargs)
       Return list of date created for all contact types.

   invoices(self, target_id=None, **kwargs)
       Returns list of dicts, key is 'DateCreated'.
       USAGE:Iterate over list from contact_idanddate() to get target_id.

   leadsources(self, **kwargs)
       Return leadsource for contacts. Number of contacts is limit key.

   tags(self, **kwargs)
       Return tags for target contact.

   ----------------------------------------------------------------------
   Data descriptors inherited from Query:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class Output(builtins.object)**
   Take data ready for output. Methods to write to file.

   Static methods defined here:

   as3rdparty(self, queryfunc, filename)
       ' to send to pandas, matplotlib, etc etc

   ascsv(targlist)
       Pass in result of query as list of dicts from query. Alternately, use
       elif to pass result objects in different forms to the one function,
       or to several similar functions contained in Output class.

   ascsvdict(item)
       Item arg is list of dicts. Like ascsv but with DictWriter class.

   asfile(target=None, query=None, filename='dataserv.csv')
       primarily to send to spreadsheet. TODO: use csv module

   ashtml(self, queryfunc, filename)

   asimage(self, queryfunc, filename)

   ----------------------------------------------------------------------
   Data descriptors defined here:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class Process(builtins.object)**
   Raw query data processed here for target output. Primary method to use
   is procarray(), but others are used for specific cases.

   Static methods defined here:

   combine_list(*lists)
       Pass in arbitrary number of lists, zip em all up!

   procarray(array)
       IS api returns list of entries for each query. Pass the whole array
       in here to format ready for output.

   procdate(key, dictionary)
       Pass a dictionary with "DateCreated" key, strip out date as YYYYMMDD
       without converting object type.

   procdict(dictionary)
       IS api returns entries as dicts, here if/elif/else is used to
       filter entries by keys.

   ----------------------------------------------------------------------
   Data descriptors defined here:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)

**class Query(builtins.object)**
   Create connection to API and run basic queries.

   Methods defined here:

   __init__(self)
       Instantiate Infusionsoft object and create connection to
       account app.

   ----------------------------------------------------------------------
   Data descriptors defined here:

   __dict__
       dictionary for instance variables (if defined)

   __weakref__
       list of weak references to the object (if defined)
