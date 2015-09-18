import pandas as pd
import os
from dataserv import RAW_DATA_DIR, LocalDB

raw_data = os.listdir( RAW_DATA_DIR )
currency_columns = LocalDB.currencycolumncheck
date_columns = LocalDB.datecolumncheck
conv_str2date = LocalDB.str2dateconv
encodings = {
            'iso' : 'ISO-8859-1',
            'utf' : 'utf-8',
            'win' : 'cp1252',
            }
currency = 'AUD'

def dframe_dateconv(dframe, col):
    ''' Go through date columns and convert to date format.
        dframe is a pandas dataframe object, col is target column of type string.
    '''
    for row in range(0, len(dframe[col])):
        dframe[col][row] = conv_str2date(dframe[col][row])

def dframe_currencystrip(dframe, col, currency=currency):
    '''Iterate through a pandas dataframe stripping off currency codes and
    recast to float type. Pass in col and code as strings.
    '''

    dframe.loc[:, col] = dframe[col].str.strip(code)
    dframe.loc[:, col] = dframe[col].str.strip('-' + code)
    dframe.loc[:, col] = dframe[col].str.replace(',', '')
    dframe.loc[:, col] = dframe[col].astype(float)
    return dframe

def make_sheets():
    ''' Goes through files in RAW_DATA_DIR and returns
        a dict of:
        {filename: pandas.DataFrame(filename)}
    '''
    data_sheets = {}
    for enc in encodings:
        try:
            data_sheets = {datafile.split()[0]: pd.read_csv(datafile) for datafile in raw_data}
            break
        except UnicodeDecodeError:
            data_sheets = {datafile.split()[0]: pd.read_csv(datafile, encoding=encodings[enc]) for datafile in raw_data}
            break
        except UnicodeDecodeError:
            continue  # looks silly but allows attempt at next encoding in dict
    return data_sheets

def clean_sheets(currency = currency):
    ''' Uses make_sheets(), and then processes to convert money from string to float,
        and datetime strings into datetime objects.
        Returns a dict of:
        {filename: pandas.DataFrame(filename)}
    '''
    data_sheets = make_sheets()
    for dframe in data_sheets:
        for col in dframe.keys():
            if currency_columns(col) == True:
                dframe_currencystrip(dframe, col, currency=currency)
            if date_columns(col) == True:
                dframe_dateconv(dframe, col)
    return data_sheets
