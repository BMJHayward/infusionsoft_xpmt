'''
TODO: use
unittest.mock
import cgi
cgi.test() to test script with HTTP headers and HTML.
    See docs.python.org/3/library/cgi.html
'''
import unittest, sys, os
from datetime import datetime
import sqlite3
import xmlrpc.client as client
import dataserv as iq

iqcxn = iq.Query()
iqout = iq.Output()
iqext = iq.Extract()
iqprc = iq.Process()
iqlts = iq.LeadtimetoSale()
iqlt2 = iq.Leadtime()
iqldb = iq.LocalDB()


class TestLocalDB(unittest.TestCase):

    def test_sendto_sqlite(self):
        db = ":memory:"
        queryarray1 = {a:b for a,b in vars().items()}
        queryarray2 = [x for x in range(99)]
        error_args1 = dict(query_array = queryarray1, newtable = [], db = db)
        error_args2  =  dict(query_array = {'derp', 1,54.54}, newtable = 'mixedset', db = db)
        args1  =  dict(db = db, query_array = queryarray1, newtable = 'queryarray1')
        args2  =  dict(db = db, query_array = queryarray2, newtable = 'queryarray2')
        try:
            self.assertRaises(Exception, iqldb.sendto_sqlite, **error_args1)
        except TypeError as t_err:
            print('TypeError: {0}'.format(t_err))
        except AttributeError as att_err:
            print('AttributeError: {0}'.format(att_err))
        else: print('Everything fine.')

        try:
            self.assertRaises(Exception, iqldb.sendto_sqlite, **error_args2)
        except TypeError as t_err:
            print('TypeError: {0}'.format(t_err))
        except AttributeError as att_err:
            print('AttributeError: {0}'.format(att_err))
        else: print('Everything fine.')

        try:
            iqldb.sendto_sqlite(**args1)
        except TypeError as t_err:
            print('TypeError: {0}'.format(t_err))
        except AttributeError as att_err:
            print('AttributeError: {0}'.format(att_err))
        else: print('Everything fine.')

        try:
            iqldb.sendto_sqlite(**args2)
        except TypeError as t_err:
            print('TypeError: {0}'.format(t_err))
        except AttributeError as att_err:
            print('AttributeError: {0}'.format(att_err))
        else: print('Everything fine.')

    def test_sendto_json(self):
        filename = 'test.json'
        query_array = [[i for i in range(20)],locals(), sys.modules]
        try:
            iqldb.sendto_json(query_array, filename)
        except Exception as exc:
            print('Error: {0}'.format(exc))

    def test_get_csv(self):
        try:
            csvdata = iqldb.get_csv('dataserv.csv')
            self.assertIsInstance(csvdata, list)
        except Exception as exc:
            print('Error: {0}'.format(exc))

    # def test_get_invoicedates(self):
        # try:
            # invlist = iqldb.get_invoicedates()
            # self.assertIsInstance(invlist, dict)
        # except Exception as exc:
            # print('Error: {0}'.format(exc))


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


class TestLeadtimeToSale(unittest.TestCase):

    def test_leadtime_to_sale(self):
        ltslist = iqlts.leadtime()
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

    def test_procarray(self):

        sample_list = iqext.leadsources()
        iqprc.procarray(sample_list)
        print(sample_list)
        self.assertIsNotNone(sample_list)
        self.assertIs(type(sample_list), list)

    def test_procdict(self):

        dates = iqext.dates()
        for date in dates:
            iqprc.procdict(date)
        for date in dates:
            for value in date.values():
                self.assertIs(type(value), datetime)


class TestOutput(unittest.TestCase):

    def test_asfile(self):

        test_msg = iqout.asfile()
        self.assertIs(type(test_msg), str)


class TestLeadtime(unittest.TestCase):


    def test_stats_leadtime(self):
        pass
    def test_get_leadtime(self):
        pass
    def test_get_data(self):
        contactsales = iqlt2.get_data()
        require_keys = ['invdates', 'entrydate', 'leadtime']
        wrong_keys = ['data', 123, r'invdates', u'invdates']

        try:
            self.assertIsInstance(contactsales, dict)
        except TypeError as t_err:
            print('TypeError: {0}'.format(t_err))

        for key in contactsales:
            try:
                self.assertIsInstance(contactsales[key], dict)
            except TypeError as t_err:
                print('TypeError: {0}'.format(t_err))
            except Exception as exc:
                print('Exception: {0}'.format(exc))
            try:
                for required in require_keys:
                    self.assertTrue(required in contactsales[key].keys())
            except AssertionError as ass_err:
                print('AssertionError: {0}'.format(ass_err), required)
            try:
                for wrong in wrong_keys:
                    self.assertTrue(wrong in contactsales[key].keys())
            except AssertionError as ass_err:
                print('AssertionError: {0}: '.format(ass_err), 'Wrong key: ', wrong, ' , key type: ',type(wrong))

    def test_get_db_table(self):
        pass
    def test_list_convert(self):
        pass
    def test_leadtime_from_db(self):
        pass

    def test_convert_datestring(self):
        now = datetime.now()
        now = client.DateTime(now)
        td_a = '19/6/2009'
        td_b = '19/06/2009'
        td_c = '20080627T14:40:14'
        td_d = now
        trgdates = [td_a, td_b, td_c, td_d]

        for date in trgdates:
            try:
                iqlt2.convert_datestring(date)
            except TypeError as t_err:
                print('AttributeError: {0}'.format(t_err))
            except AttributeError as att_err:
                print('AttributeError: {0}'.format(att_err))
            except Exception as exc:
                print('AttributeError: {0}'.format(exc))


if __name__ == '__main__':
    unittest.main()
