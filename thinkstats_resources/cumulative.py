"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import first
import descriptive
import math
import Cdf
import Pmf
import survey
import thinkstats

import matplotlib.pyplot as pyplot
import myplot


def Process(table, name):
    """Runs various analyses on this table.

    Creates instance variables:
        weights: sequence of int total weights in ounces
        weight_pmf: Pmf object
        weight_cdf: Cdf object
        oz_pmf: Pmf of just the ounce field
    """
    descriptive.Process(table, name)

    table.weights = [p.totalwgt_oz for p in table.records
                     if p.totalwgt_oz != 'NA']
    table.weight_pmf = Pmf.MakePmfFromList(table.weights, table.name)
    table.weight_cdf = Cdf.MakeCdfFromList(table.weights, table.name)


def MakeTables(data_dir):
    """Reads survey data and returns a tuple of Tables"""
    table, firsts, others = first.MakeTables(data_dir)
    pool = descriptive.PoolRecords(firsts, others)

    Process(pool, 'live births')
    Process(firsts, 'first babies')
    Process(others, 'others')
        
    return pool, firsts, others


def Resample(cdf, n=10000):
    sample = cdf.Sample(n)
    new_cdf = Cdf.MakeCdfFromList(sample, 'resampled')
    myplot.Cdfs([cdf, new_cdf],
                root='resample_cdf',
                title='CDF',
                xlabel='weight in oz',
                ylabel='CDF(x)') 


def MakeExample():
    """Make a simple example CDF."""
    t = [2, 1, 3, 2, 5]
    cdf = Cdf.MakeCdfFromList(t)
    myplot.Cdf(cdf,
              root='example_cdf',
              title='CDF',
              xlabel='x',
              ylabel='CDF(x)',
              axis=[0, 6, 0, 1],
              legend=False)    


def MakeFigures(pool, firsts, others):
    """Creates several figures for the book."""

    bar_options = [
        dict(linewidth=0, color='blue'),
        dict(linewidth=0, color='orange')
        ]

    # plot PMFs of birth weights for first babies and others
    myplot.Hists([firsts.weight_pmf, others.weight_pmf], 
               root='nsfg_birthwgt_pmf',
               bar_options=bar_options, 
               title='Birth weight PMF',
               xlabel='weight (ounces)',
               ylabel='probability')

    plot_options = [
                    dict(linewidth=2, color='blue'),
                    dict(linewidth=2, color='orange')
                    ]

    # plot CDFs of birth weights for first babies and others
    myplot.Cdfs([firsts.weight_cdf, others.weight_cdf], 
               root='nsfg_birthwgt_cdf',
               plot_options=plot_options, 
               title='Birth weight CDF',
               xlabel='weight (ounces)',
               ylabel='probability',
               axis=[0, 200, 0, 1])

def main(name, data_dir=''):
    MakeExample()

    pool, firsts, others = MakeTables(data_dir)
    MakeFigures(pool, firsts, others)
    

if __name__ == '__main__':
    import sys
    main(*sys.argv)
