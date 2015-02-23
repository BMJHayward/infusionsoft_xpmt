"""
TODO: use
import cgi
cgi.test()
to test script with HTTP headers and HTML. See docs.python.org/3/library/cgi.html
"""

""" create connection to API, test data service and query function """
import iteratequestionnaire as iq
iqcxn = iq.InfusionQuery()

def sampleQuery( ):
        """ makes 4 queries returning date created, leadsource and tags (groups) """
        table = 'Contact'
        returnFields = ['DateCreated', 'Leadsource']
        query = {'ContactType' : '%'}
        limit = 10
        page = 0
        datesource = iqcxn.infusionsoft.DataService('query', 'Contact', \
                    10, 0, {'ContactType' : '%'}, ['DateCreated','Leadsource'])

        print( iqcxn.infusionsoft.DataService( 'query', table, limit, \
                    page, query, returnFields ))

def fullStringQuery_a():
        print(iqcxn.infusionsoft.DataService('query', 'Contact', 10, 0, \
                     {'ContactType' : '%'}, ['DateCreated','Leadsource'])) # returns an array of dicts

def fullStringQuery_b():
        print(iqcxn.infusionsoft.DataService('query', 'Contact', 10, 0, \
                    {'ContactType' : '%'}, ['Groups'])) # get tags with 'Groups' field from 'Contact' table

def main():

    tests = {'sample' : sampleQuery, 'query_a' : fullStringQuery_a, 'query_b' : fullStringQuery_b}

    for test in tests.keys():
        try:
            tests[test]()
        except Exception as detail:
            print("query failed: " + test + ", ", detail)

if __name__ == '__main__':
    main()
