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
iqprc = iq.Process()
iqlts = iq.LeadtimetoSale()

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

    def test_querytags(self):

        data = iqext.tags()
        self.assertIs(type(data), list)

    def test_querydate(self):

        data = iqext.dates()
        self.assertIs(type(data), list)

    def test_queryleadsource(self):

        data = iqext.leadsources()
        self.assertIs(type(data), list)

    def test_invoices(self):

        targ_id = 1000
        inv_arg = dict(limit=9)
        inv_list = iqext.invoices(targ_id, **inv_arg)
        self.assertIs(type(inv_list), list)

    def test_cost_sale_leadsource(self):

        pass

    def test_average_transaction_value(self):

        pass

    def test_customer_lifetime_value(self):

        pass

class TestLeadtimeToSale(unittest.TestCase):

    def test_leadtime_to_sale(self):
        ltslist = iqlts.leadtime_to_sale()
        for dic in ltslist:
            self.assertTrue('Invoices' in dic and
            'DateCreated' in dic and
            'Id' in dic
            )

    def test_iddates(self):
        datelist = iqlts.iddates()
        for dic in datelist:
            self.assertTrue('Id' in dic and 'DateCreated' in dic)

    def test_get_inv(self):
        invlist = iqlts.get_inv(11)  # using 11 as dummy id
        for dic in invlist:
            self.assertTrue('DateCreated' in dic)


class TestProcess(unittest.TestCase):
    ''' test query data is processed correctly '''

    def test_iter_array(self):

        sample_list = iqext.leadsources()
        lead_list = iqprc.iter_array(sample_list)
        print(lead_list)
        self.assertIsNotNone(lead_list)
        self.assertIs(type(lead_list), list)

    def test_query_process(self):

        tags = iqext.tags()
        taglist = []
        for  tag in tags:
            taglist.extend([iqprc.procdict(key, tag) for key in tag.keys()])
        for tag in taglist:
            self.assertIs(type(tag), int)

        dates = iqext.dates()
        datelist = [iqprc.procdict(date) for date in dates]
        for date in datelist:
            self.assertIs(type(date), int)

        sources = iqext.leadsources()
        srclist = [iqprc.procdict(src) for src in sources]
        for src in srclist:
            self.assertIs(type(src), str)

class TestOutput(unittest.TestCase):

    def test_asfile(self):

        test_msg = iqout.asfile()
        self.assertIs(type(test_msg), str)


if __name__ == '__main__':
    unittest.main()
