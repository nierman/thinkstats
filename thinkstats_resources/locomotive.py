"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

This file contains a solution to the locomotive problem adapted from 
Mosteller, Fifty Challenging Problems in Probability:

"A railroad numbers its locomotives in order 1..N.  One day you see a 
locomotive with the number 60.  Estimate how many locomotives the 
railroad has."

"""

import matplotlib.pyplot as pyplot
import myplot
import Pmf
import Cdf
from math import pow


def MakeUniformSuite(low, high, steps):
    """Makes a PMF that represents a suite of hypotheses with equal p.
    
    Args:
        low: low end of range
        high: high end of range
        steps: number of values

    Returns:
        Pmf object
    """
    hypos = [low + (high-low) * i / (steps-1.0) for i in range(steps)]
    pmf = Pmf.MakePmfFromList(hypos)
    return pmf


def Update(suite, evidence):
    """Updates a suite of hypotheses based on new evidence.

    Modifies the suite directly; if you want to keep the original, make
    a copy.

    Args:
        suite: Pmf object
        evidence: whatever kind of object Likelihood expects
    """
    for hypo in suite.Values():
        likelihood = Likelihood(evidence, hypo)
        suite.Mult(hypo, likelihood)
    suite.Normalize()


def Likelihood(evidence, hypo):
    """Computes the likelihood of the evidence assuming the hypothesis is true.

    Args:
        evidence: a tuple of (number of heads, number of tails)
        hypo: float probability of heads

    Returns:
        probability of tossing the given number of heads and tails with a
        coin that has p probability of heads
    """
    train_seen = evidence
    num_trains = hypo
    if train_seen > num_trains:
        return 0.0
    else:
        return 1.0 / num_trains


def CredibleInterval(pmf, percentage):
    """Computes a credible interval for a given distribution.

    If percentage=90, computes the 90% CI.

    Args:
        pmf: Pmf object representing a posterior distribution
        percentage: float between 0 and 100

    Returns:
        sequence of two floats, low and high
    """
    cdf = Cdf.MakeCdfFromDict(pmf.GetDict())
    prob = (1 - percentage/100.0) / 2
    interval = [cdf.Value(p) for p in [prob, 1-prob]]
    return interval


def main():
    upper_bound = 200
    prior = MakeUniformSuite(1, upper_bound, upper_bound)
    prior.name = 'prior'

    evidence = 60
    posterior = prior.Copy()
    Update(posterior, evidence)
    posterior.name = 'posterior'

    print CredibleInterval(posterior, 90)

    # plot the posterior distribution
    pyplot.subplots_adjust(wspace=0.4, left=0.15)
    plot_options = dict(linewidth=2)

    myplot.Pmf(posterior, 
               plot_options=plot_options,
               root='locomotive',
               title='Locomotive problem',
               xlabel='Number of trains',
               ylabel='Posterior probability',
               show=False)

if __name__ == '__main__':
    main()
