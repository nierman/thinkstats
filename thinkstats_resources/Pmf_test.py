"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import unittest
import thinkstats
import Pmf
import Cdf

class Test(unittest.TestCase):

    def testHist(self):
        t = [1, 2, 2, 3, 5]
        hist = Pmf.MakeHistFromList(t)

        self.assertEquals(hist.Freq(1), 1)
        self.assertEquals(hist.Freq(2), 2)
        self.assertEquals(hist.Freq(3), 1)
        self.assertEquals(hist.Freq(4), 0)
        self.assertEquals(hist.Freq(5), 1)
        
        pmf = Pmf.MakePmfFromHist(hist)

        pmf.Print()
        self.checkPmf(pmf)

    def checkPmf(self, pmf):
        self.assertAlmostEquals(pmf.Prob(1), 0.2)
        self.assertAlmostEquals(pmf.Prob(2), 0.4)
        self.assertAlmostEquals(pmf.Prob(3), 0.2)
        self.assertAlmostEquals(pmf.Prob(4), 0.0)
        self.assertAlmostEquals(pmf.Prob(5), 0.2)

    def testMakePmf(self):
        t = [1, 2, 2, 3, 5]
        pmf = Pmf.MakePmfFromList(t)
        self.checkPmf(pmf)

        d = pmf.GetDict()
        self.assertAlmostEquals(d[2], 0.4)
        
        vals = pmf.Values()
        self.assertEquals(sorted(vals), [1, 2, 3, 5])

        items = pmf.Items()
        d = dict(items)
        new_pmf = Pmf.MakePmfFromDict(d)
        self.checkPmf(new_pmf)

    def testSetAndNormalize(self):
        pmf = Pmf.Pmf()
        t = [1, 2, 2, 3, 5]
        for x in t:
            pmf.Set(x, 1)
        pmf.Incr(2)
        pmf.Normalize()
        self.checkPmf(pmf)
        
    def testIncrAndNormalize(self):
        pmf = Pmf.Pmf()
        t = [1, 2, 2, 3, 5]
        for x in t:
            pmf.Incr(x)
        pmf.Normalize()
        self.checkPmf(pmf)
        
    def testMultAndNormalize(self):
        t = [1, 2, 3, 5]
        pmf = Pmf.MakePmfFromList(t)
        pmf.Mult(2, 2)
        pmf.Normalize()
        self.checkPmf(pmf)
        
    def testRender(self):
        t = [1, 2, 2, 3, 5]
        pmf = Pmf.MakePmfFromList(t)
        xs, ps = pmf.Render()

        d = dict(zip(xs, ps))
        new_pmf = Pmf.MakePmfFromDict(d)
        self.checkPmf(new_pmf)

    def testMeanAndVar(self):
        t = [1, 2, 2, 3, 5]
        mu = thinkstats.Mean(t)
        var = thinkstats.Var(t, mu)
        
        pmf = Pmf.MakePmfFromList(t)
        mu2 = pmf.Mean()
        var2 = pmf.Var()
        var3 = pmf.Var(mu2)
        
        self.assertAlmostEquals(mu, mu2)
        self.assertAlmostEquals(var, var2)
        self.assertAlmostEquals(var, var3)

    def testMakePmfFromCdf(self):
        t = [1, 2, 2, 3, 5]
        pmf = Pmf.MakePmfFromList(t)
        self.checkPmf(pmf)

        cdf = Cdf.MakeCdfFromPmf(pmf)
        pmf2 = Pmf.MakePmfFromCdf(cdf)
        self.checkPmf(pmf2)

if __name__ == "__main__":
    unittest.main()
