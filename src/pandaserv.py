import pandas as pd
import os
from dataserv import RAW_DATA_FILE

encodings = {
            'enc_iso' : 'ISO-8859-1',
            'enc_utf' : 'utf-8',
            'enc_win' : 'cp1252',
            }

raw_data = os.listdir( RAW_DATA_FILE )

data_sheets = []
try:
    data_sheets = [pd.read_csv(datafile) for datafile in raw_data]
except UnicodeDecodeError:
    for encs in encodings:
        data_sheets = [pd.read_csv(datafile, encoding=enc) for datafile in raw_data]
