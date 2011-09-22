"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import myplot
import Pmf
import thinkstats

from math import exp

"""This file contains a partial solution to a problem from
MacKay, "Information Theory, Inference, and Learning Algorithms."

    Unstable particles are emitted from a source and decay at a
distance $x$, a real number that has an exponential probability
distribution with [parameter] $\lambda$.  Decay events can only be
observed if they occur in a window extending from $x=1$ cm to $x=20$
cm.  $N$ decays are observed at locations $\{ 1.5, 2, 3, 4, 5, 12 \}$
cm.  What is $\lambda$?

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
        suite.Mult(hypo, likelihood)
    suite.Normalize()


def Likelihood(evidence, hypo):
    """Computes the likelihood of the evidence assuming the hypothesis is true.

    Args:
        evidence: sequence of measurements
        hypo: parameter of the expo distribution

    Returns:
        probability of the evidence under the hypothesis
    """
    param = hypo
    likelihood = 1
    for x in evidence:
        likelihood *= ExpoCondPdf(x, param)

    return likelihood


def ExpoCondPdf(x, param, low=1.0, high=20.0):
    """Evaluates the conditional exponential PDF.

    Returns the probability density of x in the exponential PDF
    with the given parameter, with the condition that low < x < high.

    Args:
      x: float observed value
      param: float parameter of the exponential distribution
      low: float, low end of the observable range
      high: float, high end of the observable range
    """
    factor = exp(-low * param) - exp(-high * param)
    p = param * exp(-param * x) / factor
    return p


def main():
    suite = MakeUniformSuite(0.001, 1.5, 1000)
    evidence = [1.5, 2, 3, 4, 5, 12]

    Update(suite, evidence)
    suite.name = 'posterior'

    # plot the posterior distributions
    myplot.Pmf(suite, 
               title='Decay parameter',
               xlabel='Parameter (inverse cm)',
               ylabel='Posterior probability',
               show=True)

    print 'Naive parameter estimate:', 1.0 / thinkstats.Mean(evidence)
    print 'Mean of the posterior distribution:', suite.Mean()

if __name__ == '__main__':
    main()
