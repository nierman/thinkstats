"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""

import math
import matplotlib.pyplot as pyplot
import myplot
import Pmf
import random
import thinkstats


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
        likelihood *= ExpoPdf(x, param)

    return likelihood


def ExpoPdf(x, param):
    """Evaluates the exponential PDF.

    Returns the probability density of x in the exponential PDF
    with the given parameter.

    Args:
      x: float observed value
      param: float parameter of the exponential distribution
    """
    p = param * math.exp(-param * x)
    return p


def EstimateParameter(prior, sample, name='posterior'):
    """Computes the posterior distribution for the parameter of an expo dist.

    Args:
      prior: Pmf that maps values of lamdba to their prior prob
      sample: sequence of values drawn from expo dist
      name: string name for the posterior

    Returns:
      new Pmf object with the posterior probabilities
    """
    posterior = prior.Copy()
    posterior.name = name
    Update(posterior, sample)
    return posterior


def main():

    # make a uniform prior
    param = 1.2
    prior = MakeUniformSuite(0.5, 1.5, 1000)

    # try out the sample in the book
    t = []
    sample = [2.675, 0.198, 1.152, 0.787, 2.717, 4.269]
    name = 'post%d' % len(sample)
    posterior = EstimateParameter(prior, sample, name)
    t.append(posterior)

    # try out a range of sample sizes
    for n in [10, 20, 40]:

        # generate a sample
        sample = [random.expovariate(param) for _ in range(n)]
        name = 'post%d' % n

        # compute the posterior
        posterior = EstimateParameter(prior, sample, name)
        t.append(posterior)

    # plot the posterior distributions
    for i, posterior in enumerate(t):
        pyplot.subplot(2, 2, i+1)
        myplot.Pmf(posterior,
                   title='Parameter Estimation',
                   xlabel='lambda',
                   ylabel='Posterior probability'
                   )
    myplot.Save(root='posteriors')

if __name__ == '__main__':
    main()
