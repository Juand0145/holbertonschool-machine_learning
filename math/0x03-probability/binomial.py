#!/usr/bin/env python3
"""File that contain the class that represents an
binomial distribution"""


class Binomial:
    """Class that represents an binomial distribution"""
    e = 2.7182818285
    pi = 3.1415926536

    def __init__(self, data=None, n=1, p=0.5):
        if data is None:
            if n <= 0:
                raise ValueError("n must be a positive value")
            if p >= 1 or p <= 0:
                raise ValueError("p must be greater than 0 and less than 1")
            self.n = n
            self.p = p

        else:
            if type(data) is not list:
                raise TypeError("data must be a list")
            if len(data) < 2:
                raise ValueError("data must contain multiple values")

            mean = sum(data) / len(data)
            variance = sum([(x - mean) ** 2 for x in data]) / len(data)
            self.p = 1 - (variance/mean)
            n = mean/self.p
            self.n = round(n)
            self.p *= n/self.n

    def pmf(self, k):
        """Binomial distribution pmf"""
        k = int(k)
        if k > self.n and k < 0:
            return 0

        pmf = (factorial(self.n) / factorial(k) / factorial(self.n - k) *
               self.p ** k * (1 - self.p) ** (self.n - k))
        return pmf

    def cdf(self, k):
        """Binomial distribution cdf"""
        pmf = []
        if k < 0:
            return 0
        k = int(k)

        for n in range(k + 1):
            pmf.append(self.pmf(n))

        CDF = sum(pmf)
        return CDF


def factorial(n):
    """Function to calculate the factorial from a number"""
    if n < 2:
        return 1
    return n * factorial(n-1)
