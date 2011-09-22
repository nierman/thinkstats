"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import unittest
import Cdf

class Test(unittest.TestCase):

    def testMakeCdfFromList(self):
        t = [2, 1, 3, 2, 5]
        cdf = Cdf.MakeCdfFromList(t, 'bob')
        self.checkCdf(cdf)

    def checkCdf(self, cdf):
        self.assertEqual(cdf.xs, [1, 2, 3, 5])
        self.assertEqual(cdf.ps, [0.2, 0.6, 0.8, 1.0])
        self.assertEqual(cdf.name, 'bob')

    def testProb(self):
        t = [2, 1, 3, 2, 5]
        cdf = Cdf.MakeCdfFromList(t, 'bob')

        self.assertEqual(cdf.Prob(-1), 0.0)
        self.assertEqual(cdf.Prob(1), 0.2)
        self.assertEqual(cdf.Prob(2), 0.6)
        self.assertEqual(cdf.Prob(2.5), 0.6)
        self.assertEqual(cdf.Prob(4), 0.8)
        self.assertEqual(cdf.Prob(5), 1.0)
        self.assertEqual(cdf.Prob(7), 1.0)

    def testValue(self):
        t = [2, 1, 3, 2, 5]
        cdf = Cdf.MakeCdfFromList(t, 'bob')

        self.assertEqual(cdf.Value(0.0), 1)
        self.assertEqual(cdf.Value(0.1), 1)
        self.assertEqual(cdf.Value(0.2), 1)
        self.assertEqual(cdf.Value(0.3), 2)
        self.assertEqual(cdf.Value(0.4), 2)
        self.assertEqual(cdf.Value(0.5), 2)
        self.assertEqual(cdf.Value(0.6), 2)
        self.assertEqual(cdf.Value(0.7), 3)
        self.assertEqual(cdf.Value(0.8), 3)
        self.assertEqual(cdf.Value(0.9), 5)
        self.assertEqual(cdf.Value(1.0), 5)
        self.assertRaises(ValueError, cdf.Value, -0.1)
        self.assertRaises(ValueError, cdf.Value, 1.1)

    def testMean(self):
        t = [2, 1, 3, 2, 5]
        cdf = Cdf.MakeCdfFromList(t, 'bob')
        self.assertAlmostEqual(cdf.Mean(), 13.0/5.0)

    def testItems(self):
        t = [2, 1, 3, 2, 5]
        cdf = Cdf.MakeCdfFromList(t, 'bob')

        items = cdf.Items()
        expected = [(1, 0.2), (2, 0.6), (3, 0.8), (5, 1.0)]
        for p1, p2 in zip(items, expected):
            for x1, x2 in zip(p1, p2):
                self.assertEqual(x1, x2)
        
    def testRender(self):
        t = [2, 1, 3, 2, 5]
        cdf = Cdf.MakeCdfFromList(t, 'bob')

        vs, ps = cdf.Render()
        self.assertEqual(vs, [1, 1, 2, 2, 3, 3, 5, 5])
        for got, expected in zip(ps, [0.0, 0.2, 0.2, 0.6, 0.6, 0.8, 0.8, 1.0]):
            self.assertAlmostEqual(got, expected)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCdf']
    unittest.main()
