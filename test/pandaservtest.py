import unittest, sys, os
from datetime import datetime
import pandas as pd
import src.pandaserv as pandaserv
import numpy as np


class Testpandaserv(unittest.TestCase):

    def setUp(self):
        self.dates = pd.date_range('20130101', periods=6)
        self.df = pd.DataFrame(
                    np.random.randn(6,4), index=self.dates, columns=list('ABCD'))
        self.df2 = pd.DataFrame({ 'A' : 1.,
                                  'B' : pd.Timestamp('20130102'),
                                  'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                                  'D' : np.array([3] * 4,dtype='int32'),
                                  'E' : pd.Categorical(["test","train","test","train"]),
                                  'F' : '20140101' })

    def test_dframe_dateconv(self):
        print('Unfinished test, PASS.')
        pandaserv.dframe_dateconv(self.df2, 'F')
        for singledate in range(0, len(self.df2['F'])):
            self.assertIsInstance(self.df2['F'][singledate], datetime)

    def test_dframe_currencystrip(self):
        print('Unfinished test, PASS.')

    def test_make_sheets(self):
        print('Unfinished test, PASS.')

    def test_clean_sheets(self):
        print('Unfinished test, PASS.')


if __name__ == '__main__':
    unittest.main()