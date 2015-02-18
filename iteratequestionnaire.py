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

answers = { # increment score when cutomer has tags in 'yes' and 'sometimes' arrays, take maximum score as result
    'tinnitus_yes': [ 1796, 1826, 1856, 1886 ],
    'tinnitus_no': [ 1800, 1830, 1860, 1890 ],
    'tinnitus_sometimes': [ 1798, 1828, 1858, 1888 ],

    'hearing_yes': [ 1808, 1838, 1868, 1898  ],
    'hearing_no': [ 1812, 1842, 1872, 1902 ],
    'hearing_sometimes': [ 1810, 1840, 1870, 1900 ],

    'hyperacusis_yes': [ 1802, 1832, 1862, 1892 ],
    'hyperacusis_no': [ 1806, 1836, 1866, 1896 ],
    'hyperacusis_sometimes': [ 1804, 1834, 1864, 1894 ],

    'dizziness_yes': [ 1814, 1844, 1874, 1904 ],
    'dizziness_no': [ 1818, 1848, 1878, 1908 ],
    'dizziness_sometimes': [ 1816, 1846, 1876, 1906 ],

    'blockear_yes': [ 1820, 1850, 1880, 1910  ],
    'blockear_no': [ 1824, 1854, 1884, 1914 ],
    'blockear_sometimes': [ 1822, 1852, 1882, 1912 ],
    }

score_array = { # increment score when cutomer has tags in 'yes' and 'sometimes' arrays, take maximum score as result
    'tinnitus_yes': 0,
    'tinnitus_no': 0,
    'tinnitus_sometimes': 0,

    'hearing_yes': 0,
    'hearing_no': 0,
    'hearing_sometimes': 0,

    'hyperacusis_yes': 0,
    'hyperacusis_no': 0,
    'hyperacusis_sometimes': 0,

    'dizziness_yes': 0,
    'dizziness_no': 0,
    'dizziness_sometimes': 0,

    'blockear_yes': 0,
    'blockear_no': 0,
    'blockear_sometimes': 0,
    }

tag_result = { "tinnitus" : 2278, "hyperacusis" : 2280, "hearing" : 2282,  "dizziness" : 2284, "blockear" : 2286 }

def score_update( target ):
    if key.contains( 'yes' ):
        score_array[ target ] += 5
    elif key.contains( 'some' ):
        score_array[ target ] += 3
    else:
        return

def check_tag( cust_tag, target_tag ):
    if cust_tag == target_tag:
        score_update( answers.get(key) )
    else:
        return

def iterate():
    cust_tag = infusionQuery.querytags()
    for answer in answers.values():
        for ans in answer:
            check_tag( cust_tag, ans )


def iterateandAppend( list ): # this will be used to compare answers with people's answers. print(tag) will change later to something useful
    # can maybe use a comprehension like at end of this function, not sure yet
    for value in answers.values():
        for tag in value:
            list.append( tag )
    answers_list = [ tag for values in answers.values() for tag in values ]

# import infusionsoft
class infusionQuery( ):
    """ creates a connection, runs basic queries.
        using 'iqcxn' to name the infusionQuery object in shell
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

        # for line in dateandSource[]:
        #     for key,value in line:
        #         x.write(key,value)
        # x.close()

"""
# TODO: write this output to csv or text file
for iter in itertools.tee(iqcxn.dateandSource):
    for it in iter:
        print(it) # gives dict of datecreated and leadsource for each contact in dateandSource object.
"""

def getDates():
    """
    Pull out individual dates so arrays of leadsource with dates can be analysed.
    NOTE: some contacts don't have a date created, so yymmdd will return an array shorter than 
    the value of total_contacts.
    """
    iqcxn = infusionQuery()
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
