'''
TODO: use
unittest.mock
import cgi
cgi.test() to test script with HTTP headers and HTML.
    See docs.python.org/3/library/cgi.html
'''
import unittest
import dataserv as iq

iqcxn = iq.Query()


class TestQuery(unittest.TestCase):
    ''' this class may be just to test InfusionQuery() class, with new test
        class for each component class
    '''

    def test_sampleQuery(self):
        ''' make 4 queries returning date created, leadsource and tags '''
        table = 'Contact'
        returnFields = ['DateCreated', 'Leadsource']
        query = {'ContactType': '%'}
        limit = 10
        page = 0

        print(iqcxn.infusionsoft.DataService('query', table, limit,
              page, query, returnFields))


    def test_fullStringQuery_a(self):

        print(iqcxn.infusionsoft.DataService('query', 'Contact', 10, 0,
              {'ContactType': '%'}, ['DateCreated', 'Leadsource']))


    def test_fullStringQuery_b(self):

        print(iqcxn.infusionsoft.DataService('query', 'Contact', 10, 0,
              {'ContactType': '%'}, ['Groups']))


    def test_querytags(self):

        data = iqcxn.tags()
        print(data)


    def test_querydate(self):

        data = iqcxn.dates()
        print(data)


    def test_queryleadsource(self):

        data = iqcxn.leadsources()
        print(data)


    def test_basequery(self):

        defaultData = iqcxn._basequery()
        self.assertIsNotNone(defaultData)
        self.assertIs(type(defaultData), list)


    def test_basequerywithdata(self):

        altargs = dict(table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['DateCreated'])
        altdata = iqcxn._basequery(**altargs)
        self.assertIsNotNone(altdata)
        self.assertIs(type(altdata), list)


    def test_count(self):

        countdata = iqcxn._count('ContactGroup', 'Id')
        self.assertIsNotNone(countdata)
        self.assertIs(type(countdata), int)


class TestProcess(unittest.TestCase):
    ''' test query data is processed correctly '''


    def test_iter_array(self):

        sample_list = iqcxn.leadsources()
        lead_list = iq.Process(sample_list)
        final_list = lead_list.iter_array()
        self.assertIsNotNone(final_list)
        self.assertIs(type(final_list), list)


    def test_query_process(self):

        tags = iq.Query().tags()
        self.assertIsNotNone(tags)
        self.assertIs(type(tags[0].get('GroupId')), int)


    def test_testlist(self):
        testlist = iq.sourcelist()
        self.assertIsNotNone(testlist)
        self.assertIs(type(testlist), list)


if __name__ == '__main__':
    unittest.main()
