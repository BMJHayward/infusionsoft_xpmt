'''
TODO:
1:put array variables, sort functions into a class
2:include all assessment tags as arrays, centralise all assessment sorting into one file, using main class
3: possible reporting function
4: sorting class to call infusionsoft class to get customer tags
5: use pandas or matplotlib for dataviz
6: statistics?
'''

from infusionsoft.library import Infusionsoft

# import infusionsoft
class InfusionQuery:
    ''' creates a connection, runs basic queries. '''

    def __init__( self ):
        ''' instantiates Infusionsoft API object, and creates connection to account app from local textfile credentials '''

        self.key = [line for line in open('APIKEY.txt') ][ 0 ]
        self.appName = [line for line in open('APPNAME.txt') ][ 0 ]
        self.infusionsoft = Infusionsoft( self.appName, self.key )

    def querytags(self, ContactId=154084, recordcount=10 ):
        ''' returns tags for target contact '''
        self.tags = self.infusionsoft.DataService(
        'query','ContactGroupAssign',recordcount,0,{'ContactId':str(ContactId)},['GroupId']
        )

        return self.tags

    def querydate(self, recordcount=10):
        ''' returns list of date created for contacts totalling recordcount arg '''
        self.date = self.infusionsoft.DataService(
        'query','Contact',recordcount,0,{'ContactType':'%'},['DateCreated'])

        return self.date

    def queryleadsource(self, recordcount=10):
        self.leadsource = self.infusionsoft.DataService(
        'query','Contact', recordcount,0,{'ContactType':'%'},['Leadsource'])

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

    def make_list(self, data):

        raise NotImplementedError


class OutputData:
    ''' expects target_list to be of type list '''

    def writetofile(self, target_list = None, queryfunc=None, filename='dataserv.csv'):
        ''' primarily to send to spreadsheet. TODO: probably replace this with csv module '''

        if target_list != None:
            self.data = target_list
        elif queryfunc != None:
            self.data = queryfunc

        with open(filename,'a+') as self.tempfile:
            for line in self.data:
                self.tempfile.write(line)
                self.tempfile.write(",")
                self.tempfile.write("\n")
                print(line)

    def writetohtml(self, queryfunc, filename):
        raise NotImplementedError

    def writetoimage(self, queryfunc, filename):
        raise NotImplementedError

    def writeto3rdparty(self, queryfunc, filename):
        '''' to send to pandas, matplotlib, etc etc '''
        raise NotImplementedError

def makecsvlist(dict):

    csvlist = [ ]
    for item in iter(dict):
        if item == 'DateCreated':
            csvlist.append(str(dict[item]).split('T')[0])
        elif item == 'Leadsource':
            csvlist.append(dict[item])
        #elif item == 'Address'
          #  csvlist.append(dict[item])

    return csvlist # give 2D (future: n-D) list back to caller to write to desired output

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
    dates = eval(open('dates.txt','r+').read())
    from collections import Counter
    datescount = Counter(dates)


def writetofile(sourcelist):


    for item in sourcelist:
        makecsvlist(item)
    x = [makecsvlist(item) for item in sourcelist]

    file  = open('dateandsource.csv','w+')
    for item in x:
         file.write(str(item)+'\n')
    file.close()

def sourcelist():

    testlist = InfusionQuery().getDateandsource()

    return testlist
