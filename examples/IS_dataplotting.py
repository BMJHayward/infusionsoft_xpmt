
# coding: utf-8

# In[3]:

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sbrn


# In[4]:

monthly_sales = pd.read_csv(r'S:\Program Files (x86)\Users\SERVER-MEDIA\Downloads\monthsales.csv')


# In[5]:

monthly_sales.head()


# In[6]:

monthly_sales['Amt sold']


# In[7]:

monthly_sales.loc[:, 'Amt sold'] = monthly_sales['Amt sold'].str.strip('AUD')
monthly_sales.loc[:, 'Amt sold'] = monthly_sales['Amt sold'].str.strip('-AUD')
monthly_sales.loc[:, 'Amt sold'] = monthly_sales['Amt sold'].str.replace(',', '')
monthly_sales.loc[:, 'Amt sold'] = monthly_sales['Amt sold'].astype(float)
monthly_sales.head()


# In[8]:

type(monthly_sales['Amt sold'][3])


# In[9]:

def numToMonth(num):
    return{
        1 : 'Jan',
        2 : 'Feb',
        3 : 'Mar',
        4 : 'Apr',
        5 : 'May',
        6 : 'Jun',
        7 : 'Jul',
        8 : 'Aug',
        9 : 'Sep',
        10 : 'Oct',
        11 : 'Nov',
        12 : 'Dec'
        }[num]


# In[10]:

monthly_sales = monthly_sales.drop(monthly_sales.index[22])


# In[11]:

monthly_sales.loc[:, 'month'] = monthly_sales['month'].map(numToMonth)


# In[12]:

monthly_sales['Amt sold'][:-1].plot.bar()
plt.ylabel('Monthly revenue')
plt.show()


# In[14]:

monthly_sales.plot.bar(x='month', y='Amt sold')
plt.show()


# In[ ]:

def salesplot(dframe, x_axis, y_axis):
    if x_axis == 'month':
        dframe.loc[:, x_axis] = dframe[x_axis].map(numToMonth)
    dframe.plot.bar(x=x_axis, y=y_axis)
    plt.show()
