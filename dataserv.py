'''
TODO:
1: put array variables, sort functions into a class
2: include all assessment tags as arrays, centralise all assessment sorting
   into one file, using main class
3: possible reporting function
4: sorting class to call infusionsoft class to get customer tags
5: use pandas or matplotlib for dataviz
6: statistics?
'''

from infusionsoft.library import Infusionsoft


class Query:
    ''' creates a connection, runs basic queries. '''

    def __init__(self):
        ''' instantiates Infusionsoft API object, and creates connection to
            account app from local textfile credentials
        '''

        self.key = [line for line in open('APIKEY.txt')][0]
        self.appName = [line for line in open('APPNAME.txt')][0]
        self.infusionsoft = Infusionsoft(self.appName, self.key)


    def _basequery(self, **kwargs):
        ''' allows query to be written in one place
            kwargs allows override of args
        '''
        self.default = dict(
            table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['City','State','Country']
            )

        if kwargs is not None:
            self.default.update(kwargs)

        try:
            self.data = self.infusionsoft.DataService(
                'query', self.default['table'],
                self.default['limit'], self.default['page'],
                self.default['queryData'], self.default['returnData']
                )

            return self.data

        except Exception as exc:

            print('Error running query: ', exc)


    def _count(self, table, query):
        ''' returns number of entries in table to retrieve all data
            returns int, use as limit to iterate queries, append to list results
        '''

        self.count = self.infusionsoft.DataService('count', table, {query: '%'})

        return self.count

    def _getpages(self, table, query):
        ''' returns total pages to search through when using dataservice '''

        self.totalrecords = self._count(table, query)
        self.pages = (self.totalrecords//999 + 1)

        return self.pages

    def tags(self, **kwargs):
        ''' returns tags for target contact '''

        self.tagargs = dict(
            table='ContactGroupAssign',
            limit=10,
            page=0,
            queryData={'ContactId': '154084'},
            returnData=['GroupId']
            )

        if kwargs is not None:
                    self.tagargs.update(kwargs)

        self.tag = self._basequery(**self.tagargs)

        return self.tag


    def dates(self, **kwargs):
        ''' returns list of date created for all contact types '''

        self.dateargs = dict(
            table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['DateCreated']
            )

        if kwargs is not None:
                    self.dateargs.update(kwargs)

        self.date = self._basequery(**self.dateargs)

        return self.date


    def leadsources(self, **kwargs):

        self.sourceargs = dict(
            table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['Leadsource']
            )

        if kwargs is not None:
                    self.sourceargs.update(kwargs)

        self.leadsource = self._basequery(**self.sourceargs)

        return self.leadsource


class Process:
    ''' raw query data processed here for target output'''

    def __init__(self, array):

        self.array = array


    def iter_array(self):

        data = []
        for dictionary in self.array:
            data.append(self.query_process(dictionary))

        return data


    def query_process(self, dictionary):

        if 'GroupId' in dictionary.keys():

            tag = dictionary['GroupId']
            return tag

        elif 'DateCreated' in dictionary.keys():
            date = str(dictionary['DateCreated'])
            date = date.split('T')[0]
            date = int(date)

            return date

        elif 'Leadsource' in dictionary.keys():

            lead = dictionary['Leadsource']
            return lead


    def combine_list(self, *lists):

        ziplist = zip(*lists)
        ziplist = list(ziplist)
        return ziplist


class Output:
    ''' expects target_list to be of type list '''

    def asfile(self, target=None, query=None, filename='dataserv.csv'):
        ''' primarily to send to spreadsheet. TODO: use csv module '''

        self.data = None
        if target is not None:
            self.data = target
        elif query is not None:
            self.data = query

        with open(filename, 'a+') as self.tempfile:
            for line in self.data:
                self.tempfile.write(repr(line))
                self.tempfile.write(",")
                self.tempfile.write("\n")
                print(line)

    def asscv(self, queryfunc, filename):

        # import csv
        # with open(filename, newline="") as source;
            # rdr= DictReader(source)
            # data = list(rdr)
            # return data

        raise NotImplementedError

    def ashtml(self, queryfunc, filename):
        raise NotImplementedError


    def asimage(self, queryfunc, filename):
        raise NotImplementedError


    def as3rdparty(self, queryfunc, filename):
        '''' to send to pandas, matplotlib, etc etc '''
        raise NotImplementedError


def histogram():
    '''
    using bokeh to visualise:
    from bokeh.plotting import figure, output_file, show
    output_file('histogram.html')
    p = figure(title = 'insert title')
    x = datescount.keys()
    y = datescount.values()
    p.line(x,y)
    show(p)
    '''
    dates = eval(open('dates.txt', 'r+').read())
    from collections import Counter
    datescount = Counter(dates)


def sourcelist():

    testlist = [Query().dates(), Query().tags(), Query().leadsources()]

    return testlist
