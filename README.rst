########################
Infusionsoft Experiment
########################

Using the command pattern to abstract over the data service portion of the Infusionsoft API (Infusionsoft a.ka. 'IS' from here on).

DESCRIPTION
############

Extract, transform, load data from IS, send to excel, csv, pandas, matplotlib, numpy etc.
This project will keep to the stdlib where ever possible to minimise dependencies, and simplify deployment in several environments.


dataserv.py is the main file of interest for the moment. this may be broken up in future as more classes are added.

TODO:
#####

+ include recordcount() to return all data when using 'all' argument
+ refactor Query() methods to use basequery() method
+ experiment with and write tests for Query.basequery() method
+ use pandas or matplotlib for dataviz
+ statistics

CLASSES
########
    builtins.object
        Output
        Process
        Query
    
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
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
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
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Query(builtins.object)
     |  creates a connection, runs basic queries.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      instantiates Infusionsoft API object, and creates connection to
     |      account app from local textfile credentials
     |  
     |  dates(self, recordcount=10)
     |      returns list of date created for all contact types
     |  
     |  leadsources(self, recordcount=10)
     |  
     |  tags(self, ContactId=154084, recordcount=10)
     |      returns tags for target contact
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FUNCTIONS
##########

    histogram()
        using bokeh to visualise:
        from bokeh.plotting import figure, output_file, show
        output_file('histogram.html')
        p = figure(title = 'insert title')
        x = datescount.keys()
        y = datescount.values()
        p.line(x,y)
        show(p)
    
    sourcelist()

