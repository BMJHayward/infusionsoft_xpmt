import numpy as np
import scipy as sp
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sbrn
import datetime
import dateutil
import sys, os
import xlrd, xlwt


dateparse = dateutil.parser.parse


csv_file = r'S:\Program Files (x86)\Users\SERVER-MEDIA\Downloads\sale_per_leadsource_2008_2015.csv'
smallcsv_file = r'S:\Program Files (x86)\Users\SERVER-MEDIA\Downloads\sales_2015.csv'
xl_file = r'S:\Program Files (x86)\Users\SERVER-MEDIA\Downloads\sales_leadsources_2008_2015.xlsx'
monthly_sales = pd.read_csv(csv_file, parse_dates=[2], index_col=[2], low_memory=False)

monthly_sales.head()

monthly_sales.loc[:, 'Inv Total'] = monthly_sales['Inv Total'].str.strip('AUD')
monthly_sales.loc[:, 'Inv Total'] = monthly_sales['Inv Total'].str.strip('-AUD')
monthly_sales.loc[:, 'Inv Total'] = monthly_sales['Inv Total'].str.replace(',', '')
monthly_sales.loc[:, 'Inv Total'] = monthly_sales['Inv Total'].astype(float)
monthly_sales.head()

salespivot = pd.pivot_table(monthly_sales, index=monthly_sales.index, columns=['Lead Source'], values=['Inv Total'])
plt.figure(); plt.plot(salespivot.T); plt.show()

pivotfile = r'S:\Program Files (x86)\Users\SERVER-MEDIA\Downloads\salespivot.csv'
salespivot.to_csv(path_or_buf=pivotfile)

salespivot.plot(stacked=True,x=salespivot.index,y=salespivot.columns)
plt.figure()
plt.legend(salespivot.columns.tolist())
plt.plot_date(salespivot.index, salespivot, '.', xdate=True, ydate=False, aa=True)
plt.show()



monthly_sales.plot('Inv Total')
salespivot = pd.pivot_table(monthly_sales,index=monthly_sales.index, columns=['Lead Source'],values=['Inv Total'])
plt.figure(); plt.plot(salespivot.T); plt.show()
salespivot = pd.pivot_table(monthly_sales,index=monthly_sales.index, columns=['Lead Source'],values=['Inv Total'])
plt.figure(); plt.plot(salespivot); plt.show()
