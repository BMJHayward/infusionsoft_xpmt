import pandas as pd
import os
from dataserv import RAW_DATA_DIR, LocalDB

raw_data = os.listdir( RAW_DATA_FILE )
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
    data_sheets = []
    try:
        data_sheets = [pd.read_csv(datafile) for datafile in raw_data]
    except UnicodeDecodeError:
        for encs in encodings:
            data_sheets = [pd.read_csv(datafile, encoding=enc) for datafile in raw_data]
    return data_sheets

def clean_sheets(currency = currency):
    data_sheets = make_sheets()
    for dframe in data_sheets:
        for col in dframe.keys():
            if currency_columns(col) == True:
                dframe_currencystrip(dframe, col, currency=currency)
            if date_columns(col) == True:
                dframe_dateconv(dframe, col)

