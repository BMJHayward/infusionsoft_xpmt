"""
TODO:
1:put array variables, sort functions into a class
2:include all assessment tags as arrays, centralise all assessment sorting into one file, using main class
3: possible reporting function
4: sorting class to call infusionsoft class to get customer tags
5: use pandas or matplotlib for dataviz
6: statistics?
"""

from infusionsoft.library import Infusionsoft

# import infusionsoft
class InfusionQuery( ):
    """ creates a connection, runs basic queries.
        using 'iqcxn' to name the InfusionQuery object in shell
     """

    def __init__( self ):
        """ this class will get app name and api key from text file, create connection, and run a query for you """

        self.key = [line for line in open('APIKEY.txt') ][ 0 ]
        self.appName = [line for line in open('APPNAME.txt') ][ 0 ]
        self.infusionsoft = Infusionsoft( self.appName, self.key )

    def querytags(self, recordcount=10 ):
        """ use this to do contactTags=querytags(contact_id) """
        self.tags = self.infusionsoft.DataService(
        'query','ContactGroupAssign',recordcount,0,{'ContactId':'154084 '},['GroupId']
        )

        return self.tags

    def querydate(self, recordcount=10):
        self.date = self.infusionsoft.DataService(
        'query','Contact',recordcount,0,{'ContactType':'%'},['DateCreated'])

        return self.date

    def queryleadsource(self, recordcount=10):
        self.leadsource = self.infusionsoft.DataService(
        'query','Contact', recordcount,0,{'ContactType':'%'},['Leadsource'])

        return self.leadsource

    def writetofile(self, queryfunc, filename):
        """ need write to file to send to excel """
        # attempting to get contact data, write it to file
        self.data = queryfunc
        self.tempfile = open(filename,'a+')
        for line in self.data:
            self.tempfile.write(str(line))
            print( line ) # this returns a dict for each line, datetime is its own object. WTF infusionsoft!?!
        self.tempfile.close()

    def getdateandsource(self):
        self.dateandsource = self.infusionsoft.DataService('query','Contact',10,0,{'ContactType':'%'},['DateCreated','Leadsource'])
        print("captured dateandsource object...")
        print("object type: ", type(self.dateandsource))
        print("object length: ", len(self.dateandsource))
        print( str(self.dateandsource[0]['DateCreated']).split('T')[0] ) # to get date yymmdd as string

        return self.dateandsource

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

def makecsvlist(dict):

    list = [ ]
    for item in iter(dict):
        if item == 'DateCreated':
            list.append(str(dict[item]).split('T')[0])
        elif item == 'Leadsource':
            list.append(dict[item])
        #elif item == 'Address'
          #  list.append(dict[item])

    return list # give 2D (future: n-D) list back to caller to write to desired output

def writetofile(sourcelist):


    for item in sourcelist:
        makecsvlist(item)
    x = [makecsvlist(item) for item in sourcelist]

    file  = open('dateandsource.csv','w+')
    for item in x:
         file.write(str(item)+'\n')
    file.close()

def sourcelistlist():

    testlist = InfusionQuery().getDateandsource()

    return testlist
