'''
TODO:
1:put array variables, sort functions into a class
2:include all assessment tags as arrays, centralise all assessment sorting into
    one file, using main class
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
        default = dict(
            table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['City','State','Country']
            )

        if kwargs is not None:
            for kwarg in kwargs.keys():
                self.default[kwarg] = kwargs[kwarg]

        try:
            self.data = self.infusionsoft.DataService(
                'query', default['table'], default['limit'], default['page'],
                default['queryData'], default['returnData']
                )

            return self.data

        except Exception as exc:
            print('Error running query: ', exc)


    def tags(self, ContactId=154084, recordcount=10):
        ''' returns tags for target contact '''
        self.tag = self.infusionsoft.DataService(
            'query', 'ContactGroupAssign', recordcount, 0,
            {'ContactId': str(ContactId)}, ['GroupId']
            )

        return self.tag

    def dates(self, recordcount=10):
        ''' returns list of date created for all contact types '''
        self.date = self.infusionsoft.DataService(
            'query', 'Contact', recordcount, 0,
            {'ContactType': '%'}, ['DateCreated']
            )

        return self.date

    def leadsources(self, recordcount=10):
        self.leadsource = self.infusionsoft.DataService(
            'query', 'Contact', recordcount, 0,
            {'ContactType': '%'}, ['Leadsource']
            )

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

    testlist = InfusionQuery().getDateandsource()

    return testlist
