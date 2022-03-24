#!/usr/bin/env python3
"""File that contains the function posterior"""
from scipy import special


def posterior(x, n, p1, p2):
    """
    x is the number of patients that develop severe side effects
    n is the total number of patients observed
    p1 is the lower bound on the range
    p2 is the upper bound on the range
    You can assume the prior beliefs of p follow a uniform distribution
    """
    if type(n) is not int or n <= 0:
        raise ValueError("n must be a positive integer")
    if type(x) is not int or x < 0:
        raise ValueError(
            "x must be an integer that is greater than or equal to 0")
    if x > n:
        raise ValueError("x cannot be greater than n")
    if type(p1) is not float or p1 < 0 or p1 > 1:
        raise ValueError("p1 must be a float in the range [0, 1]")
    if type(p2) is not float or p2 < 0 or p2 > 1:
        raise ValueError("p2 must be a float in the range [0, 1]")
    if p2 <= p1:
        raise ValueError("p2 must be greater than p1")

    beta_dist1 = special.btdtr(x + 1, n - x + 1, p1)

    beta_dist2 = special.btdtr(x + 1, n - x + 1, p2)

    posterior = beta_dist2 - beta_dist1
    return posterior
