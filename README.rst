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
+ use CSV module to write to file
+ composition basic query objects for use in reporting class
+ possible Report() class for inidividual reports to inherit from
+ use pandas or matplotlib for dataviz
+ statistics?

CLASSES
########

    builtins.object
        Output
        Process
        Query
            Extract
                AvgerageTransactionValue
                ContactIdAndDate
                CostSaleLeadsource
                CustomerLifetimeValue
                LeadtimeToSale
    
    class AvgerageTransactionValue(Extract)
     |  Retrun average amount of transaction across all products.
     |  TODO: segment by time period, leadsource, product etc.
     |  
     |  Method resolution order:
     |      AvgerageTransactionValue
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  average_transaction_value(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Extract:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Query:
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
   
    class ContactIdAndDate(Extract)
     |  Return array of contact ids with date created. Most analysis will need
     |  to cross-reference this data.
     |  
     |  Method resolution order:
     |      ContactIdAndDate
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  contact_idanddate(self, **kwargs)
     |      returns Id AND DateCreated at once for cross-reference later
     |  
     |  contact_invoices(self, id_list=None, inv_list=None)
     |      combine date from contact_idanddate() and invoices()
     |  
     |  invoices(self, target_id=None, **kwargs)
     |      iterate over list from contact_idanddatecreated() to get target_id
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Extract:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Query:
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
 
    class CostSaleLeadsource(Extract)
     |  Return a cost per sale per leadsource object.
     |  
     |  Method resolution order:
     |      CostSaleLeadsource
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  cost_sale_leadsource(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Extract:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Query:
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
  
    class CustomerLifetimeValue(Extract)
     |  Calculate how much any given customer spends on average long term.
     |  
     |  Method resolution order:
     |      CustomerLifetimeValue
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  customer_lifetime_value(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Extract:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Query:
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
   
    class Extract(Query)
     |  Pull mass data for analysis using Query() as base. Intended as layer
     |  between direct queries and each report class.
     |  
     |  Method resolution order:
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Query:
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
    
    class LeadtimeToSale(Extract)
     |  'Return length of time from gaining a lead to making first sale.
     |  TODO: Use histograms and other stats to analyse this.
     |  
     |  Method resolution order:
     |      LeadtimeToSale
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  leadtime_to_sale(self)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Extract:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Query:
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
   
    class Output(builtins.object)
     |  expects target_list to be of type list
     |  
     |  Methods defined here:
     |  
     |  as3rdparty(self, queryfunc, filename)
     |      ' to send to pandas, matplotlib, etc etc
     |  
     |  asfile(self, target=None, query=None, filename='dataserv.csv')
     |      primarily to send to spreadsheet. TODO: use csv module
     |  
     |  ashtml(self, queryfunc, filename)
     |  
     |  asimage(self, queryfunc, filename)
     |  
     |  asscv(self, queryfunc, filename)
     |  
     |  ----------------------------------------------------------------------
   
    class Process(builtins.object)
     |  raw query data processed here for target output
     |  
     |  Methods defined here:
     |  
     |  __init__(self, array)
     |  
     |  combine_list(self, *lists)
     |  
     |  iter_array(self)
     |  
     |  query_process(self, dictionary)
     |  
     |  ----------------------------------------------------------------------
    
    class Query(builtins.object)
     |  Create connection to API and run basic queries.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Instantiate Infusionsoft object and create connection to
     |      account app.
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  
     |  ----------------------------------------------------------------------
