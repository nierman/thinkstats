"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

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

"""

from coin import *    


def IntegrateLikelihood(evidence, suite, step):
    """Computes the integral of the likelihood over all hypothesis in suite.

    Args:
      evidence: some representation of the evidence
      suite: Pmf object that maps possible parameters to their probabilities
      step: float step size between parameters in the suite

    Returns:
      float
    """
    total = 0.0
    for hypo in suite.Values():
        likelihood = Likelihood(evidence, hypo)
        total += likelihood * suite.Prob(hypo)

    return total


def main():
    n = 101
    low = 0.0
    high = 1.0
    step = (high-low) / (n-1)
    suite = MakeUniformSuite(low, high, n)
    evidence = 140, 110

    likelihood_unbiased = Likelihood(evidence, 0.5)
    print likelihood_unbiased

    likelihood_biased = IntegrateLikelihood(evidence, suite, step)
    print likelihood_biased

    ratio = likelihood_biased / likelihood_unbiased
    print ratio

    
if __name__ == '__main__':
    main()
