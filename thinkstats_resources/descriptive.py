"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import first
import math
import Pmf
import survey
import thinkstats

import matplotlib.pyplot as pyplot
import myplot


def Process(table, name):
    """Runs various analyses on this table."""
    first.Process(table)
    table.name = name

    table.var = thinkstats.Var(table.lengths, table.mu)
    table.trim = thinkstats.TrimmedMean(table.lengths)

    table.hist = Pmf.MakeHistFromList(table.lengths, name=name)
    table.pmf = Pmf.MakePmfFromHist(table.hist)
        
        
def PoolRecords(*tables):
    """Construct a table with records from all tables.
    
    Args:
        constructor: init method used to make the new table
    
        tables: any number of tables

    Returns:
        new table object
    """
    pool = survey.Pregnancies()
    for table in tables:
        pool.ExtendRecords(table.records)
    return pool


def MakeTables(data_dir):
    """Reads survey data and returns a tuple of Tables"""
    table, firsts, others = first.MakeTables(data_dir)
    pool = PoolRecords(firsts, others)

    Process(pool, 'live births')
    Process(firsts, 'first babies')
    Process(others, 'others')
        
    return pool, firsts, others


def Summarize(pool, firsts, others):
    """Print various summary statistics."""
    
    print
    print 'Variance'
    print 'First babies', firsts.var 
    print 'Others', others.var

    diff_mu = firsts.mu - others.mu

    print 'Difference in mean', diff_mu

    sigma = math.sqrt(pool.var)

    print 'Pooled mean', pool.mu
    print 'Pooled variance', pool.var
    print 'Pooled sigma', sigma

    print firsts.mu, others.mu
    print firsts.trim, others.trim
    
    live_lengths = pool.hist.GetDict().items()
    live_lengths.sort()
    print 'Shortest lengths:'
    for weeks, count in live_lengths[:10]:
        print weeks, count
    
    print 'Longest lengths:'
    for weeks, count in live_lengths[-10:]:
        print weeks, count
    

def MakeFigures(firsts, others):
    """Plot Hists and Pmfs for the pregnancy length."""

    # bar options is a list of option dictionaries to be passed to myplot.bar
    bar_options = [
        dict(color='0.9'),
        dict(color='blue')
        ]

    # make the histogram
    axis = [23, 46, 0, 2700]
    myplot.Hists([firsts.hist, others.hist], 
                 root='nsfg_hist', 
                 title='Histogram',
                 xlabel='weeks',
                 ylabel='frequency',
                 axis=axis,
                 bar_options=bar_options
                 )

    # make the PMF
    axis = [23, 46, 0, 0.6]
    myplot.Hists([firsts.pmf, others.pmf],
                 root='nsfg_pmf',
                 title='PMF',
                 xlabel='weeks',
                 ylabel='probability',
                 bar_options=bar_options,
                 axis=axis)


def MakeDiffFigure(firsts, others):
    """Plot the difference between the PMFs."""

    weeks = range(35, 46)
    diffs = []
    for week in weeks:
        p1 = firsts.pmf.Prob(week)
        p2 = others.pmf.Prob(week)
        diff = 100 * (p1 - p2)
        diffs.append(diff)

    pyplot.clf()
    pyplot.bar(weeks, diffs, align='center')
    myplot.Save('nsfg_diffs',
              title='Difference in PMFs',
              xlabel='weeks',
              ylabel='100 (PMF$_{first}$ - PMF$_{other}$)',
              legend=False)


def main(name, data_dir=''):
    pool, firsts, others = MakeTables(data_dir)
    Summarize(pool, firsts, others)
    MakeFigures(firsts, others)
    MakeDiffFigure(firsts, others)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
