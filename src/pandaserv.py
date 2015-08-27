import pandas as pd
import os

from dataserv import RAW_DATA_FILE

raw_data = os.listdir( RAW_DATA_FILE )

data_sheets = [pd.read_csv(datafile) for datafile in raw_data]
