"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

Credits:

erf is a modified version of a function contributed to the public
domain by John D. Cook
http://www.johndcook.com/python_erf.html
"""

import math

def erf(x):
    """Evaluates the error function at x.
    
    This function is based on an algorithm in the Handbook of 
    Mathematical Functions, edited by  Milton Abramowitz and
    Irene A. Stegun, Equation 7.1.26
    
    Args:
        x: float
        
    Returns:
        float
    """
    # constants
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    # Save the sign of x
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)

    # A & S 7.1.26
    t = 1.0 / (1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)

    return sign*y

def NormalCdf(x, mu, sigma):
    """Evaluates the CDF of the normal distribution.
    
    Args:
        x: float

        mu: mean parameter
        
        sigma: standard deviation parameter
                
    Returns:
        float
    """
    y = (erf((x - mu) / float(sigma) / math.sqrt(2.0)) + 1.0) / 2.0
    return y
