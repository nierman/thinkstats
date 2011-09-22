"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import myplot
import Pmf
from math import pow

"""This file contains a partial solution to a problem from
MacKay, "Information Theory, Inference, and Learning Algorithms."

    Exercise 3.15 (page 50): A statistical statement appeared in
    "The Guardian" on Friday January 4, 2002:

        When spun on edge 250 times, a Belgian one-euro coin came
        up heads 140 times and tails 110.  'It looks very suspicious
        to me,' said Barry Blight, a statistics lecturer at the London
        School of Economics.  'If the coin weere unbiased, the chance of
        getting a result as extreme as that would be less than 7%.'

MacKay asks, "But do these data give evidence that the coin is biased
rather than fair?"

We will get to that question, but we will start by defining a distribution
of possible values for p, the probability of heads, and computing the
posterior distribution of p given the evidence cited.

The code below uses a Pmf object to represent a suite of hypotheses.
In this case, the values in the Pmf are possible values of p, but in
general we could use any kind of object to represent a hypothesis.

"""

    
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
        print hypo, likelihood
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
    heads, tails = evidence
    p = hypo
    return pow(p, heads) * pow(1-p, tails)

def main():
    suite = MakeUniformSuite(0.0, 1.0, 11)
    evidence = 140, 110

    Update(suite, evidence)
    suite.name = 'posterior'

    # plot the posterior distributions
    myplot.Pmf(suite, 
               title='Biased coin',
               xlabel='P(heads)',
               ylabel='Posterior probability',
               show=True)

if __name__ == '__main__':
    main()
