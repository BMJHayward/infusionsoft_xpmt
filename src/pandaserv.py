import pandas as pd
import os
try:
    from .dataserv import RAW_DATA_DIR, LocalDB
except ImportError:
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

    dframe.loc[:, col] = dframe[col].str.strip(currency)
    dframe.loc[:, col] = dframe[col].str.strip('-' + currency)
    dframe.loc[:, col] = dframe[col].str.replace(',', '')
    dframe.loc[:, col] = dframe[col].astype(float)
    return dframe


def get_raw_data(raw_data):
    ''' Pass an array of file names, returns absolute paths of those'''
    fullpaths = [os.path.join(RAW_DATA_DIR, sheet) for sheet in raw_data]
    sheetpaths = [os.path.abspath(path) for path in fullpaths]
    return sheetpaths


def make_onesheet(filepath):
    ''' Pass an array of file paths,
        returns a pandas dataframe of that file
    '''
    for enc in encodings:
        try:
            sheet = pd.read_csv(filepath)
            return sheet
        except UnicodeDecodeError:
            sheet = pd.read_csv(filepath, encoding=encodings[enc])
            return sheet
        except UnicodeDecodeError:
            continue  # looks silly but allows attempt at next encoding in dict


def make_sheets():
    ''' Goes through files in RAW_DATA_DIR and returns
        a dict of:
        {filename: pandas.DataFrame(filename)}
    '''
    fullpaths = get_raw_data(raw_data)
    data_sheets = {}
    for fpath in fullpaths:
        key = os.path.split(fpath)[1]
        data_sheets[key] = make_onesheet(fpath)
    return data_sheets


def clean_sheets(currency = currency):
    ''' Uses make_sheets(), and then processes to convert money from string to float,
        and datetime strings into datetime objects.
        Returns a dict of:
        {filename: pandas.DataFrame(filename)}
    '''
    data_sheets = make_sheets()
    for filename, dframe in data_sheets.items():
        for col in dframe.columns:
            if currency_columns(col) == True:
                dframe_currencystrip(dframe, col, currency=currency)
            if date_columns(col) == True:
                dframe_dateconv(dframe, col)
    return data_sheets


def monthToNum(date):
    '''Simple conversion of 3 letter dates to integers.
    '''
    return {
        'Jan' : 1,
        'Feb' : 2,
        'Mar' : 3,
        'Apr' : 4,
        'May' : 5,
        'Jun' : 6,
        'Jul' : 7,
        'Aug' : 8,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
        }[date]


def numToMonth(num):
    '''Convert integers to corresponding month.
    '''
    return {
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
        12 : 'Dec',
        }[num]


def basicplot(dframe, x_axis, y_axis):
    '''Plots anything against anything. Intended for sales plots.
       Column names from dfame are x and y axis, pass in as strings.
    '''
    if x_axis == 'month':
        dframe.loc[:, x_axis] = dframe[x_axis].map(numToMonth)
    dframe.plot.bar(x=x_axis, y=y_axis)
    plt.show()
