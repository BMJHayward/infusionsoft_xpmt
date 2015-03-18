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
iqout = iq.Output()
iqext = iq.Extract()

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

    def test_querytags(self):

        data = iqcxn.tags()
        self.assertIs(type(data), list)

    def test_querydate(self):

        data = iqcxn.dates()
        self.assertIs(type(data), list)

    def test_queryleadsource(self):

        data = iqcxn.leadsources()
        self.assertIs(type(data), list)

    def test_basequery(self):

        defaultData = iqcxn._basequery()
        print(defaultData)
        self.assertIsNotNone(defaultData)
        self.assertIs(type(defaultData), list)

    def test_basequerywithdata(self):

        altargs = dict(table='Contact',
            limit=10,
            page=0,
            queryData={'ContactType': '%'},
            returnData=['DateCreated'])
        altdata = iqcxn._basequery(**altargs)
        print(altdata)
        self.assertIsNotNone(altdata)
        self.assertIs(type(altdata), list)

    def test_count(self):

        countdata = iqcxn._count('ContactGroup', 'Id')
        print(countdata)
        self.assertIsNotNone(countdata)
        self.assertIs(type(countdata), int)

    def test_getpages(self):

        table = 'Contact'
        query = 'ContactType'
        pagecount = iqcxn._getpages(table, query)
        print(pagecount)
        self.assertIs(type(pagecount), int)


class TestExtract(unittest.TestCase):

    def test_cost_sale_leadsource(self):
        # raise NotImplementedError
        pass

    def test_average_transaction_value(self):
        # raise NotImplementedError
        pass

    def test_customer_lifetime_value(self):
        # raise NotImplementedError
        pass

    def test_leadtime_to_sale(self):
        # raise NotImplementedError
        pass

    def test_contact_idanddate(self):

        id_date = dict(limit=99)
        contact_with_date_list = iqext.contact_idanddate(**id_date)
        self.assertIs(type(contact_with_date_list), list)

    def test_invoices(self):

        targ_id = 1000
        inv_arg = dict(limit=99)
        inv_list = iqext.invoices(targ_id, **inv_arg)
        self.assertIs(type(inv_list), list)

    def test_contact_invoices(self):

        test_id_list = dict(limit=99)
        test_inv_list = dict(limit=99)
        cntct_invlist = iqext.contact_invoices(test_id_list, test_inv_list)
        self.assertIs(type(cntct_invlist), list)


class TestProcess(unittest.TestCase):
    ''' test query data is processed correctly '''

    def test_iter_array(self):

        sample_list = iqcxn.leadsources()
        lead_list = iq.Process(sample_list)
        final_list = lead_list.iter_array()
        print(final_list)
        self.assertIsNotNone(final_list)
        self.assertIs(type(final_list), list)

    def test_query_process(self):

        tags = iq.Query().tags()
        self.assertIsNotNone(tags)
        print(tags)
        self.assertIs(type(tags[0].get('GroupId')), int)

    def test_testlist(self):

        testlist = iq.sourcelist()
        print(testlist)
        self.assertIsNotNone(testlist)
        self.assertIs(type(testlist), list)

class TestOutput(unittest.TestCase):

    def test_asfile(self):

        test_msg = iqout.asfile()
        self.assertIs(type(test_msg), str)


if __name__ == '__main__':
    unittest.main()
