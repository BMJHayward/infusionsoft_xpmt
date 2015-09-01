import pandas as pd
import os
from dataserv import RAW_DATA_FILE

encodings = {
            'iso' : 'ISO-8859-1',
            'utf' : 'utf-8',
            'win' : 'cp1252',
            }

raw_data = os.listdir( RAW_DATA_FILE )

data_sheets = []
try:
    data_sheets = [pd.read_csv(datafile) for datafile in raw_data]
except UnicodeDecodeError:
    for encs in encodings:
        data_sheets = [pd.read_csv(datafile, encoding=enc) for datafile in raw_data]

how_to_stripcurrency = '''\
                lsroi = pd.read_csv('lsroi.csv')
                lsroi.loc[:, 'Expenses'] = float(lsroi['Expenses'].str.strip('AUD'))
                lsroi.loc[:, 'Expenses'] = float(lsroi['Expenses'].str.replace(',', ''))
                lsroi.loc[:, 'Expenses'] = lsroi['Expenses'].astype(float)\
                '''