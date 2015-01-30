"""
TODO:
1:put array variables, sort functions into a class
2:include all assessment tags as arrays, centralise all assessment sorting into one file, using main class
3: possible reporting function
4: sorting class to call infusionsoft class to get customer tags
"""

from infusionsoft.library import Infusionsoft

"""
tinnitus = [ tinnitus_yes,  tinnitus_no,  tinnitus_sometimes ]
hearing = [ hearing_yes,  hearing_no,  hearing_sometimes ]
hyperacusis = [ hyperacusis_yes,  hyperacusis_no,  hyperacusis_sometimes ]
dizziness = [ dizziness_yes,  dizziness_no,  dizziness_sometimes ]
blockear    = [ blockear_yes,  blockear_no,  blockear_sometimes ]
"""
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

# questionnaire = [ tinnitus,  hearing,  hyperacusis,  dizziness,  blockear ]
# questionnaire = numpy.array(questionnaire)

# questionnaire = { "tinnitus" : tinnitus, "hearing" : hearing, "hyperacusis" : hyperacusis, "dizziness" : dizziness, "blockedear" : blockear }

# tinnitus_yes = 0
# tinnitus_no = 1
# tinnitus_sometimes = 2

# hearing_yes = 3
# hearing_no = 4
# hearing_sometimes = 5

# hyperacusis_yes = 6
# hyperacusis_no = 7
# hyperacusis_sometimes = 8

# dizziness_yes = 9
# dizziness_no = 10
# dizziness_sometimes = 11

# blockear_yes = 12
# blockear_no = 13
# blockear_sometimes = 14

# array = []
# array[tinnitus_yes]=answers.get('tinnitus_yes')

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


def iterateandAppend(list): # this will be used to compare answers with people's answers. print(tag) will change later to something useful
    # can maybe use a comprehension like at end of this function, not sure yet
    for value in answers.values():
        for tag in value:
            list.append(tag)
    answers_list = [ tag for values in answers.values() for tag in values ]

# import infusionsoft
class infusionQuery( ):
    """ this class will get app name and api key from text file, create connection, and run a query for you """
#TODO: Query contact with dataservice, use this to graph lead source trends over time. Send this data to pandas
    # pass # placer, remove when queries all work properly
    def __init__(self):

        self.keyFile = open('APIKEY.txt')
        self.key = [line for line in self.keyFile]
        self.key = str( self.key )
        self.keyFile.close()
        self.appFile = open('APPNAME.txt')
        self.appName = [line for line in self.appFile]
        self.appName = str( self.appName )
        self.appFile.close()

    def connect(self): # probably want this as part of __init__()
        self.infusionsoft = Infusionsoft( self.appName, self.key )

    def sampleQuery(self):
        self.table = 'Contact'
        self.returnFields = ['DateCreated', 'Leadsource']
        self.query = {'ContactType' : '%'}
        self.limit = 10
        self.page = 0
        self.x = self.infusionsoft.DataService('query', 'Contact', 10, 0, {'ContactType' : '%'}, ['DateCreated','Leadsource'])

        print(self.infusionsoft.DataService('query', self.table, self.limit, self.page, self.query, self.returnFields))
        print(self.infusionsoft.DataService('query', 'Contact', 10, 0, {'ContactType' : '%'}, ['DateCreated','Leadsource'])) # returns an array of dicts
        print(self.infusionsoft.DataService('query', 'Contact', 10, 0, {'ContactType' : '%'}, ['Groups'])) # get tags with 'Groups' field from 'Contact' table

    def querytags(self):
        """ use this to do contactTags=querytags(contact_id) """
        self.contactTags = infusionsoft.DataService('query','ContactGroupAssign',999,0,{'ContactId':'154084 '},['GroupId']) # returns array of tag ids for contact
        self.singletag = contagTags[0].get('GroupId')

    def queryandwritetofile(self):
        # attempting to get contact data, write it to file
        self.dateandSource = infusionsoft.DataService('query','Contact',10,0,{'ContactType':'%'},['DateCreated','Leadsource'])
        self.x = open('dateandSource.txt','a')
        for line in dateandSource:
            x.write(line)

        # for line in dateandSource[]:
        #     for key,value in line:
        #         x.write(key,value)
        # x.close()
