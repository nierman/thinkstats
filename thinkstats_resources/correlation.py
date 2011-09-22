"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import math
import thinkstats

def Cov(xs, ys, mux=None, muy=None):
    """Computes Cov(X, Y).

    Args:
        xs: seqeuence of values
        ys: seqeuence of values
        mux: optional float mean of xs
        muy: optional float mean of ys

    Returns:
        Cov(X, Y)
    """
    if mux is None:
        mux = thinkstats.Mean(xs)
    if muy is None:
        muy = thinkstats.Mean(ys)

    total = 0.0
    for x, y in zip(xs, ys):
        total += (x-mux) * (y-muy)

    return total / len(xs)


def Corr(xs, ys):
    """Computes Cov(X, Y).

    Args:
        xs: seqeuence of values
        ys: seqeuence of values

    Returns:
        Corr(X, Y)
    """
    xbar, varx = thinkstats.MeanVar(xs)
    ybar, vary = thinkstats.MeanVar(ys)

    corr = Cov(xs, ys, xbar, ybar) / math.sqrt(varx * vary)

    return corr


def SpearmanCorr(xs, ys):
    """Computes Spearman's rank correlation.

    Args:
        xs: seqeuence of values
        ys: seqeuence of values

    Returns:
        float Spearman's correlation
    """
    xranks = MapToRanks(xs)
    yranks = MapToRanks(ys)
    return Corr(xranks, yranks)


def LeastSquares(xs, ys):
    """Computes a linear least squares fit for ys as a function of xs.

    Args:
        xs: seqeuence of values
        ys: seqeuence of values

    Returns:
        tuple of (intercept, slope)
    """
    xbar, varx = thinkstats.MeanVar(xs)
    ybar, vary = thinkstats.MeanVar(ys)

    slope = Cov(xs, ys, xbar, ybar) / varx
    inter = ybar - slope * xbar

    return inter, slope


def Residuals(xs, ys, inter, slope):
    """Computes residuals for a linear fit with parameters inter and slope.

    Args:
        xs: independent variable
        ys: dependent variable
        inter: float intercept
        slope: float slope

    Returns:
        list of residuals
    """
    res = [y - inter - slope*x for x, y in zip(xs, ys)]
    return res


def CoefDetermination(ys, res):
    """Computes the coefficient of determination (R^2) for given residuals.

    Args:
        ys: dependent variable
        res: residuals
        
    Returns:
        float coefficient of determination
    """
    ybar, vary = thinkstats.MeanVar(ys)
    resbar, varres = thinkstats.MeanVar(res)
    return 1 - varres / vary


def MapToRanks(t):
    """Returns a list of ranks corresponding to the elements in t.

    Args:
        t: sequence of numbers
    
    Returns:
        list of integer ranks, starting at 1
    """
    # pair up each value with its index
    pairs = enumerate(t)
    
    # sort by value
    sorted_pairs = sorted(pairs, key=lambda pair: pair[1])

    # pair up each pair with its rank
    ranked = enumerate(sorted_pairs)

    # sort by index
    resorted = sorted(ranked, key=lambda trip: trip[1][0])

    # extract the ranks
    ranks = [trip[0]+1 for trip in resorted]
    return ranks


def main():
    pass
    

if __name__ == '__main__':
    main()
