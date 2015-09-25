=========================
Infusionsoft Experiment
=========================

[![Build Status](https://travis-ci.org/BMJHayward/infusionsoft_xpmt.svg?branch=master)](https://travis-ci.org/BMJHayward/infusionsoft_xpmt)

DESCRIPTION
=============

API wrapper for Inonsoft CRM. Infusoft a.k.a. 'IS' frome Intended usespecifeporting not foun
Extract, transformad data from IS, send to excel, csv, pandmatplotlib, numpy 
dataserv and pandaserv are main files of interest for the mom
For target reports see classes inheriting from LocalDB, Query and Extrin dataserv.py.

TODO:
========

+ use pandas or matplotlib for IO/dataviz

HOW TO USE
============

1. Run and export 4 reports in your Infusionsoft account:
   1a. When you export these reports, ensure all the boxes are ticked under 'Choose fields to export'
   1b. Also, leave the date created fields blank to get the 'all time' results for your account
   1c. Save as CSV:
     + contacts (CRM -> Contacts -> Search -> Actions:Export -> Save as csv)
     + sales/orders (E-Commerce -> Orders -> Search -> Actions:Export -> Save as csv)
     + leadsource ROI (Marketing -> Reports -> Leadsource ROI -> Search ->Actions:Export-> Save as csv)
     + products (E-Commerce -> Products -> Actions:Export -> Save as csv)

2. Place the downloaded csv files in the same directory as dataserv.py

3. Do: '>>> python3 dataserv.py'. The terminal will ask a few questions:
    3a. Enter your preferred database name. A new database will be created. This allows you to have a few databases with different time frames if needed.
    3b. When asked the name of the contacts, sales, products and leadsource ROI files, enter the names of your downloaded CSV files from Infusionsoft
    3c. dataserv will do its thing, and will print an 'All done' when your report is ready.
    3.d You'll have a spreadsheet file named allstats.xls as the main output, with separate CSV for the 4 main reports.

4. The final 2 things are in Microsoft excel itself. When you open allstats.xls, go to the CSL tab to edit it. Select the 2nd column with (Percent profit, Dollar profit, expenses, revenue) as the header. Choose the excel function 'text to columns' from the Data tab in the ribbon. Choose the comma delimiter and then excel should split the data into 4 nice columns.

5. Use search and replace on '[', ']' to get rid of these, allowing you to make your charts and things.

6. For more data manipulation, simply create instances of each report class and send to Pandas, Numpy etc. E.g:

```
from dataserv import CostSaleLeadsource
import pandas as pd
newdata = CostSaleLeadsource().stats_CSL()
newdata_df = pd.DataFrame(newdata)

print('Do all your data things as you please')
```

NAME:
======

    src.dataserv


CLASSES:
=========

    builtins.object
        AverageTransactionValue
        LocalDB
            CostSaleLeadsource
            CustomerLifetimeValue
            Leadtime
        Output
        Process
        Query
            Extract
                LeadtimetoSale
    
    class AverageTransactionValue(builtins.object)
     |  Return average amount of transaction across all products.
     |  TODO: segment by time period, leadsource, product etc.
     |  +Wouldn't mind breaking this down for each leadsource
     |  
     |  Methods defined here:
     |  
     |  stats_ATV(self, dbname)
     |      +get all sales
     |      +get number of sales
     |      +do arithmetic mean
     |      + e.g: in SQL: SELECT AVG([Order Total]) FROM sales;
     |  

    
    class CostSaleLeadsource(LocalDB)
     |  Return a cost per sale per leadsource dictionary.
     |  
     |  Method resolution order:
     |      CostSaleLeadsource
     |      LocalDB
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  ROI_stats(self, leadsource_row)
     |      Used to create a dict of dicts with stats for each leadsource.
     |  
     |  destring_leadsourceROI_table(self, row)
     |      Might want to use named constants in to_float and to_int, but
     |      I will probably only use this here and nowhere else.
     |  
     |  stats_CSL(self, dbname)
     |      +get expenses per leadsource via API
     |      +get number of sales per leadsource via API
     |      +combine the two
     |      ^OR^
     |      +run leadsource ROI report
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from LocalDB:
     |  
     |  db_iterate(self, dbname)
     |  
     |  stripcurrencycodes(self)
     |      Iterates through databases is local directory, removes currency code,
     |      converts column to float.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from LocalDB:
     |  
     |  convert_currencystring(dbname, dbtbl, dbcol)
     |      Converts currency column in AUD to float.
     |  
     |  create_joinlisttable(dbname)
     |      Creates join of two tables. Currently on uses sales and contacts table.
     |      Might open this to other tables later.
     |  
     |  currencycolumncheck(columnname)
     |      Columns below contain currency transactions in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  date2strconv(datept)
     |      Use to write datetime objects back to db in format dd/mm/yyyy.
     |  
     |  datecolumncheck(columnname)
     |      Columns below contain dates in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  get_csv(filename)
     |      Give local csv file as string, returns a list of lists of that file.
     |  
     |  get_db_column(dbname, dbtbl, dbcol)
     |      Pass in name, table and column as string, get back the column.
     |  
     |  get_db_table(db_name, db_table)
     |      Pass in database name and table as string, get back the table.
     |  
     |  get_invoicedates(dbname)
     |      Returns list of purchase dates for each contact.
     |  
     |  sendto_json(query_array, filename)
     |      Use json to store entire query as json file.
     |  
     |  sendto_sqlite(query_array, newtable, db='dataserv.db')
     |      Use sqlite3 module to output to local DB. Saves API calls. Using text datatypes
     |      in tables to avoid type conversion for datetime objects.
     |  
     |  str2dateconv(datept)
     |      Use to take date columns from db to create datetime objects.
     |  

    
    class CustomerLifetimeValue(LocalDB)
     |  Calculate how much any given customer spends on average long term.
     |  
     |  Method resolution order:
     |      CustomerLifetimeValue
     |      LocalDB
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, dbname)
     |  
     |  stats_CLV(self)
     |      +get target contact invoices
     |      +sum value of all invoices
     |      +repeat for all contacts who have purchased
     |      +get average of all contacts lifetimevalue
     |      +wouldn't mind breaking down CLV by leadsource
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from LocalDB:
     |  
     |  db_iterate(self, dbname)
     |  
     |  stripcurrencycodes(self)
     |      Iterates through databases is local directory, removes currency code,
     |      converts column to float.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from LocalDB:
     |  
     |  convert_currencystring(dbname, dbtbl, dbcol)
     |      Converts currency column in AUD to float.
     |  
     |  create_joinlisttable(dbname)
     |      Creates join of two tables. Currently on uses sales and contacts table.
     |      Might open this to other tables later.
     |  
     |  currencycolumncheck(columnname)
     |      Columns below contain currency transactions in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  date2strconv(datept)
     |      Use to write datetime objects back to db in format dd/mm/yyyy.
     |  
     |  datecolumncheck(columnname)
     |      Columns below contain dates in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  get_csv(filename)
     |      Give local csv file as string, returns a list of lists of that file.
     |  
     |  get_db_column(dbname, dbtbl, dbcol)
     |      Pass in name, table and column as string, get back the column.
     |  
     |  get_db_table(db_name, db_table)
     |      Pass in database name and table as string, get back the table.
     |  
     |  get_invoicedates(dbname)
     |      Returns list of purchase dates for each contact.
     |  
     |  sendto_json(query_array, filename)
     |      Use json to store entire query as json file.
     |  
     |  sendto_sqlite(query_array, newtable, db='dataserv.db')
     |      Use sqlite3 module to output to local DB. Saves API calls. Using text datatypes
     |      in tables to avoid type conversion for datetime objects.
     |  
     |  str2dateconv(datept)
     |      Use to take date columns from db to create datetime objects.
     |  

    
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
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  invoices(self, target_id=None, **kwargs)
     |      Returns list of dicts, key is 'DateCreated'.
     |      USAGE:Iterate over list from contact_idanddate() to get target_id.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  

    
    class Leadtime(LocalDB)
     |  Use local database to calculate leadtime instead of API.
     |  Just call stats_leadtime(), returns dict with everything.
     |  
     |  Method resolution order:
     |      Leadtime
     |      LocalDB
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  convert_datestring(self, targetdate)
     |  
     |  get_data(self, dbname)
     |  
     |  get_leadtime(self, dbname)
     |  
     |  leadtime_from_db(self, targetlist)
     |  
     |  list_convert(self, targetlist)
     |  
     |  stats_LT(self, dbname, INCLUDE_LIST=False)
     |      Main entry point for database form of Leadtime class.
     |      Pass it nothing, get back dictionary mean, median, quintile and
     |      std deviation. Component functions listed below in order of appearance.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from LocalDB:
     |  
     |  db_iterate(self, dbname)
     |  
     |  stripcurrencycodes(self)
     |      Iterates through databases is local directory, removes currency code,
     |      converts column to float.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from LocalDB:
     |  
     |  convert_currencystring(dbname, dbtbl, dbcol)
     |      Converts currency column in AUD to float.
     |  
     |  create_joinlisttable(dbname)
     |      Creates join of two tables. Currently on uses sales and contacts table.
     |      Might open this to other tables later.
     |  
     |  currencycolumncheck(columnname)
     |      Columns below contain currency transactions in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  date2strconv(datept)
     |      Use to write datetime objects back to db in format dd/mm/yyyy.
     |  
     |  datecolumncheck(columnname)
     |      Columns below contain dates in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  get_csv(filename)
     |      Give local csv file as string, returns a list of lists of that file.
     |  
     |  get_db_column(dbname, dbtbl, dbcol)
     |      Pass in name, table and column as string, get back the column.
     |  
     |  get_db_table(db_name, db_table)
     |      Pass in database name and table as string, get back the table.
     |  
     |  get_invoicedates(dbname)
     |      Returns list of purchase dates for each contact.
     |  
     |  sendto_json(query_array, filename)
     |      Use json to store entire query as json file.
     |  
     |  sendto_sqlite(query_array, newtable, db='dataserv.db')
     |      Use sqlite3 module to output to local DB. Saves API calls. Using text datatypes
     |      in tables to avoid type conversion for datetime objects.
     |  
     |  str2dateconv(datept)
     |      Use to take date columns from db to create datetime objects.
     |  

    
    class LeadtimetoSale(Extract)
     |  Return length of time from gaining a lead to making first sale.
     |  HOW TO USE:
     |  >>> leadtime = LeadtimetoSale().leadtime()
     |  >>> Output().ascsvdict(leadtime)
     |  
     |  Method resolution order:
     |      LeadtimetoSale
     |      Extract
     |      Query
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  created_minus_sale(self, dct)
     |      Gives number of days between date of lead and date of sale.
     |  
     |  datecompare(self, xmlrpcDateCreated, xmlrpcFirstSale)
     |      Calc days between 2 dates returned from IS.
     |      Dates passed in must be xmlrpc.client.DateTime if python3.x or
     |      xmlrpclib.DateTime if python2.x. Can also use DateTime-like
     |      objects which have the timetuple() method.
     |  
     |  first_inv_date(self, dct)
     |      Pass in dict with Invoices key, returns earliest invoice date.
     |  
     |  get_daystosale(self, leadtimedict)
     |      Pass in dict from LeadtimetoSale(), returns number of days from
     |      lead generation to first purchase for that contact.
     |  
     |  get_inv(self, idarg)
     |      Returns DateCreated of invoices of id arg.
     |  
     |  iddates(self, **kwargs)
     |      Returns Id and DateCreated from Contact table as dict.
     |  
     |  leadtime(self, **kwargs)
     |      Use extract() to get data, use process() to make it sensible.
     |      Return an object useful for visualistion.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from Extract:
     |  
     |  __init__(self)
     |      Use super() to create API connection.
     |      Timeframes for reported data.
     |  
     |  dates(self, **kwargs)
     |      Return list of date created for all contact types.
     |  
     |  invoices(self, target_id=None, **kwargs)
     |      Returns list of dicts, key is 'DateCreated'.
     |      USAGE:Iterate over list from contact_idanddate() to get target_id.
     |  
     |  leadsources(self, **kwargs)
     |      Return leadsource for contacts. Number of contacts is limit key.
     |  
     |  tags(self, **kwargs)
     |      Return tags for target contact.
     |  

    
    class LocalDB(builtins.object)
     |  Methods for operating on local sqlite database.
     |  Would like report classes to be able use either Query or LocalDB in the same way. Maybe.
     |  
     |  Methods defined here:
     |  
     |  db_iterate(self, dbname)
     |  
     |  stripcurrencycodes(self)
     |      Iterates through databases is local directory, removes currency code,
     |      converts column to float.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  convert_currencystring(dbname, dbtbl, dbcol)
     |      Converts currency column in AUD to float.
     |  
     |  create_joinlisttable(dbname)
     |      Creates join of two tables. Currently on uses sales and contacts table.
     |      Might open this to other tables later.
     |  
     |  currencycolumncheck(columnname)
     |      Columns below contain currency transactions in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  date2strconv(datept)
     |      Use to write datetime objects back to db in format dd/mm/yyyy.
     |  
     |  datecolumncheck(columnname)
     |      Columns below contain dates in infusionsoft.
     |      Some of these are app specific. You will need to update
     |      to match your infusionsoft account.
     |  
     |  get_csv(filename)
     |      Give local csv file as string, returns a list of lists of that file.
     |  
     |  get_db_column(dbname, dbtbl, dbcol)
     |      Pass in name, table and column as string, get back the column.
     |  
     |  get_db_table(db_name, db_table)
     |      Pass in database name and table as string, get back the table.
     |  
     |  get_invoicedates(dbname)
     |      Returns list of purchase dates for each contact.
     |  
     |  sendto_json(query_array, filename)
     |      Use json to store entire query as json file.
     |  
     |  sendto_sqlite(query_array, newtable, db='dataserv.db')
     |      Use sqlite3 module to output to local DB. Saves API calls. Using text datatypes
     |      in tables to avoid type conversion for datetime objects.
     |  
     |  str2dateconv(datept)
     |      Use to take date columns from db to create datetime objects.
     |  

    
    class Output(builtins.object)
     |  Take data ready for output. Methods to write to file.
     |  
     |  Static methods defined here:
     |  
     |  as3rdparty(self, queryfunc, filename)
     |      ' to send to pandas, matplotlib, etc etc
     |  
     |  ascsv(targlist, outfile)
     |      Pass in result of query as list of dicts from query. Alternately, use
     |      elif to pass result objects in different forms to the one function,
     |      or to several similar functions contained in Output class.
     |  
     |  ascsvdict(item, outfile)
     |      Item arg is list of dicts. Like ascsv but with DictWriter class.
     |  
     |  asfile(target=None, query=None, filename='dataserv.csv')
     |      primarily to send to spreadsheet. Target and query do same thing, was useful
     |      to make more sense interacting with Infusionsoft API.
     |  
     |  ashtml(self, queryfunc, filename)
     |      Put in data, intended to save as valid static webpage.
     |  
     |  asimage(self, queryfunc, filename)
     |      If you just want the visual form of your data.
     |  
     |  datetime_to_excel(dateobj)
     |  
     |  stats_getall(dbname)
     |      Get return data from all report classes,
     |      return dict of reportname:data pairs.
     |  
     |  stats_outputall(dbname)
     |  
     |  strap_csvfiles()
     |  
     |  to_picklejar(data_to_save, name)
     |      Give whatever object you have to pickle, save it for your next session with given name.
     |  

    
    class Process(builtins.object)
     |  Raw query data processed here for target output.
     |  This class is really only useful when subclassing Extract.
     |  Kept here for reference for now.
     |  
     |  Methods defined here:
     |  
     |  combine_list(self, *lists)
     |  
     |  convert_date(self, IS_dateobject)
     |  
     |  procarray(self, array)
     |  
     |  procdate(self, key, dictionary)
     |  
     |  procdict(self, dictionary)
     |  
    
    class Query(builtins.object)
     |  Create connection to API and run basic queries.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Instantiate Infusionsoft object and create connection to
     |      account app.
     |  

FUNCTIONS
    importer()
        csvarray should be string including .csv extension in local folder
    
    main()
    
    make_tablename()
        takes user input at command line for csv files exported from IS
    
    remove_duplicates(headerrow)
        Infusionsoft csv files often have duplicate strings as header row.
        When importing to sql, this raises sqlite3.OperationalError. Pass in the
        first row of your csv file to fix this. importer() calls this for you as well.

DATA
    DB_DIR = 'databases'
    RAW_DATA_DIR = 'rawdata'
    RESULT_DATA_DIR = 'resultdata'

NAME
======

    src.pandaserv

FUNCTIONS
==========

    clean_sheets(currency='AUD')
        Uses make_sheets(), and then processes to convert money from string to float,
        and datetime strings into datetime objects.
        Returns a dict of:
        {filename: pandas.DataFrame(filename)}
    
    dframe_currencystrip(dframe, col, currency='AUD')
        Iterate through a pandas dataframe stripping off currency codes and
        recast to float type. Pass in col and code as strings.
    
    dframe_dateconv(dframe, col)
        Go through date columns and convert to date format.
        dframe is a pandas dataframe object, col is target column of type string.
    
    get_raw_data(raw_data)
        Pass an array of file names, returns absolute paths of those
    
    make_onesheet(filepath)
        Pass an array of file paths,
        returns a pandas dataframe of that file
    
    make_sheets()
        Goes through files in RAW_DATA_DIR and returns
        a dict of:
        {filename: pandas.DataFrame(filename)}

DATA
    RAW_DATA_DIR = 'rawdata'
    currency = 'AUD'
    encodings = {'iso': 'ISO-8859-1', 'utf': 'utf-8', 'win': 'cp1252'}
    raw_data = ['df2.csv', 'datesdf.csv', 'moneydf.csv', 'df.csv']