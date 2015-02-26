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
#TODO: Query contact with dataservice, use this to graph lead source trends over time. Send this data to pandas
    # pass # placer, remove when queries all work properly
    def __init__( self ):
        """ this class will get app name and api key from text file, create connection, and run a query for you """

        self.key = [line for line in open('APIKEY.txt') ][ 0 ]
        self.appName = [line for line in open('APPNAME.txt') ][ 0 ]
        self.infusionsoft = Infusionsoft( self.appName, self.key )

    def querytags( self ):
        """ use this to do contactTags=querytags(contact_id) """
        self.contactTags = self.infusionsoft.DataService('query','ContactGroupAssign',999,0,{'ContactId':'154084 '},['GroupId']) # returns array of tag ids for contact
        self.singletag = self.contactTags[ 0 ].get('GroupId')
        print( "Success. Tag: ", self.singletag )

    def queryandwritetofile( self ):
        """ need write to file to send to excel """
        # attempting to get contact data, write it to file
        self.dateandSource = self.infusionsoft.DataService('query','Contact',10,0,{'ContactType':'%'},['DateCreated','Leadsource'])
        self.tempfile = open('dateandSource.txt','a+')
        for line in self.dateandSource:
            self.tempfile.write(str(line))
            print( line ) # this returns a dict for each line, datetime is its own object. WTF infusionsoft!?!
        self.tempfile.close()

    def getDateandsource( self ):
        self.dateandSource = self.infusionsoft.DataService('query','Contact',10,0,{'ContactType':'%'},['DateCreated','Leadsource'])
        print("captured dateandSource object...")
        print("object type: ", type(self.dateandSource))
        print("object length: ", len(self.dateandSource))
        print( str(self.dateandSource[0]['DateCreated']).split('T')[0] ) # to get date yymmdd as string
        print( self.dateandSource[0]['Leadsource'] ) # returns leadsource name as string

        return self.dateandSource

        """
        self.x, self.y = [],[]
        self.knob = 0
        for self.knob in self.dateandSource[self.knob]:
            self.y.extend(self.knob['Leadsource'])
            self.str_date = str(self.knob['DateCreated']).split('T')[0]
            self.x.extend( int( str_date ) )
        return self.x, self.y
        """

def getDates():
    """
    Pull out individual dates so arrays of leadsource with dates can be analysed.
    NOTE: some contacts don't have a date created, so yymmdd will return an array shorter than
    the value of total_contacts.
    """
    iqcxn = InfusionQuery()
    total_contacts = iqcxn.infusionsoft.DataService('count','Contact',{'Id':'%'})
    pages = (total_contacts // 1000) + 2
    # dateandSource = iqcxn.infusionsoft.DataService('query','Contact',10,0,{'ContactType':'%'},['DateCreated'])
    dateandSource = []
    for i in range(0,pages):
        dateandSource.extend(
            iqcxn.infusionsoft.DataService('query','Contact',1000,i,{'ContactType':'%'},['DateCreated'])
            )
        print("currently at page: ", i+1, " of ", pages, " pages.")

    dates = [ list(item.values()) for item in dateandSource ]

    yymmdd=[]
    for item in range(0, len(dates)):
        yymmdd.append(str(dates[item][0]).split('T')[0])
        yymmdd[item]=int(yymmdd[item])
    return yymmdd

def getDates_sources():
    """
    Very similar to getDates(), also similar to what's in InfusionQuery() class. These will need to be merged eventuallly.
    Want to make these loosely coupled parts of a Command patttern.
    Pull out individual dates and leadsource so arrays of leadsource with dates can be analysed.
    NOTE: some contacts may not have a date or leadsource, so yymmdd will return an array shorter than
    the value of total_contacts.
    """
    iqcxn = InfusionQuery()
    total_contacts = iqcxn.infusionsoft.DataService('count','Contact',{'Id':'%'})
    pages = (total_contacts // 1000) + 2
    # dateandSource = iqcxn.infusionsoft.DataService('query','Contact',10,0,{'ContactType':'%'},['DateCreated'])
    dateandSource = []
    for i in range(0,pages):
        dateandSource.extend(
            iqcxn.infusionsoft.DataService('query','Contact',1000,i,{'ContactType':'%'},['Leadsource','DateCreated'])
            )
        print("currently at page: ", i+1, " of ", pages, " pages.")

    dates2 = [ list(item.values()) for item in dateandSource[1] ]
    sources = [list(item.values()) for item in dateandSource[0] ]

    yymmdd=[]
    for item in range(0, len(dates)):
        yymmdd.append(str(dates[item][0]).split('T')[0])
        yymmdd[item]=int(yymmdd[item])
    return yymmdd

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
    ''' call this function like this:
    for item in testlist:
        makecsvlist(item)
    '''
    for item in iter(dict):
        if item == 'DateCreated':
            print(str(dict[item]).split('T')[0])
        elif item == 'Leadsource':
            print(dict[item])

    # return list # give 2D list back to caller to write to desired output

def testlist():
    x = [ ]
    testlist = InfusionQuery().getDateandsource()

    for item in testlist:
        x.append(list(testlist[0].values()))
    with open('dates.txt','r+') as tempfile:
        for item in x:
            tempfile.write(str(item) + '\n')
    tempfile.close()

    with open('dateandsource.csv','r+') as file:
        for item in testlist:
            file.write(str(item) + '\n')
        file.close()

    return x
