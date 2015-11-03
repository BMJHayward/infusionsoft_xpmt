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
pivotcolumns =  [i[1] for i in list(salespivot)]
plt.figure(); plt.plot(salespivot.T); plt.show()

pivotfile = r'S:\Program Files (x86)\Users\SERVER-MEDIA\Downloads\salespivot.csv'
salespivot.to_csv(path_or_buf=pivotfile)

salespivot.plot(stacked=True,x=salespivot.index,y=salespivot.columns)

# Shows scatter graph with labels. Lots of labels if you have many leadsources.
plt.figure()
plt.plot_date(salespivot.index, salespivot, '.', xdate=True, ydate=False, aa=True)
plt.legend(salespivot.columns.tolist())
plt.show()

# Shows the same scattergraph but with top leadsources, in case you have too many to plot
srtd = salespivot['Inv Total'].sum()
srtd.sort()
topsources = list(srtd[-20:-1].index)
salespivot['Inv Total'][topsources]
plt.figure()
plt.plot_date(salespivot.index, salespivot['Inv Total'][topsources], '.', xdate=True, ydate=False, aa=True)
plt.legend(salespivot.columns.tolist())
plt.show()


fig, ax = plt.subplots()
plt.legend(salespivot.columns.tolist())
ax.plot(salespivot.index, salespivot, '.')
plt.show()

monthly_sales.plot('Inv Total')
salespivot = pd.pivot_table(monthly_sales,index=monthly_sales.index, columns=['Lead Source'],values=['Inv Total'])
plt.figure(); plt.plot(salespivot.T); plt.show()
salespivot = pd.pivot_table(monthly_sales,index=monthly_sales.index, columns=['Lead Source'],values=['Inv Total'])
plt.figure(); plt.plot(salespivot); plt.show()

for key in salespivot['Inv Total'].keys():
    print(key, ' : ', np.sum(salespivot['Inv Total'][key])

# get vital stats and save as html, convenient for sharing with non-pythonistas
# plus a plot, of course!
description = salespivot.describe()
with open('leadsource_description.html','w+') as descfile:
    descfile.write(description.T.to_html()
plt.figure()
description.T.plot()
plt.show()

# group leadsources
for i in salespivot['Inv Total']:print(salespivot['Inv Total'][i]

def group_leadsources(dataframe, leadsources):
    grouptotals = {'A':0,'I':0,'L':0,'B':0,'D':0,'P':0,'M':0,'LTR':0,'F':0,}
    for leadsource in leadsources:
        if 'A - ' in leadsource:
            grouptotals['A'] += dataframe[leadsource].sum()
        elif 'I - ' in leadsource:
            grouptotals['I'] += dataframe[leadsource].sum()
        elif 'L - ' in leadsource:
            grouptotals['L'] += dataframe[leadsource].sum()
        elif 'B - ' in leadsource:
            grouptotals['B'] += dataframe[leadsource].sum()
        elif 'D - ' in leadsource:
            grouptotals['D'] += dataframe[leadsource].sum()
        elif 'P - ' in leadsource:
            grouptotals['P'] += dataframe[leadsource].sum()
        elif 'M - ' in leadsource:
            grouptotals['M'] += dataframe[leadsource].sum()
        elif 'LTR - ' in leadsource:
            grouptotals['LTR'] += dataframe[leadsource].sum()
        elif 'F - ' in leadsource:
            grouptotals['F'] += dataframe[leadsource].sum()

    return grouptotals

leadsources = salespivot['Inv Total'].columns.tolist()
grouptotals = group_leadsources(salespivot['Inv Total'], leadsources)
groupdf = pd.DataFrame.from_dict(grouptotals, orient='index')
groupdf.plot(kind='bar')
plt.show()
