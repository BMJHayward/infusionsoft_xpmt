import pandas as pd
import os
from dataserv import RAW_DATA_FILE

encodings = {
            'iso' : 'ISO-8859-1',
            'utf' : 'utf-8',
            'win' : 'cp1252',
            }

raw_data = os.listdir( RAW_DATA_FILE )

def make_sheets():
    data_sheets = []
    try:
        data_sheets = [pd.read_csv(datafile) for datafile in raw_data]
    except UnicodeDecodeError:
        for encs in encodings:
            data_sheets = [pd.read_csv(datafile, encoding=enc) for datafile in raw_data]
    return data_sheets

def dframe_currencystrip(dframe, col, code='AUD'):
    '''Iterate through a pandas dataframe stripping off currency codes and
    recast to float type. Pass in col and code as strings.
    '''

    dframe.loc[:, col] = dframe[col].str.strip(code)
    dframe.loc[:, col] = dframe[col].str.strip('-' + code)
    dframe.loc[:, col] = dframe[col].str.replace(',', '')
    dframe.loc[:, col] = dframe[col].astype(float)
    return dframe