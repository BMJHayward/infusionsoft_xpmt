import pandas as pd
import os
encodings = {
            'enc_iso' : 'ISO-8859-1',
            'enc_utf' : 'utf-8',
            'enc_win' : 'cp1252',
            }

from dataserv import RAW_DATA_FILE

raw_data = os.listdir( RAW_DATA_FILE )
data_sheets = []
for encs in encodings:
    try:
        data_sheets = [pd.read_csv(datafile) for datafile in raw_data]
    except UnicodeDecodeError:
        data_sheets = [pd.read_csv(datafile, encoding=enc) for datafile in raw_data]
