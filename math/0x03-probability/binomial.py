#!/usr/bin/env python3
"""File that contain the class that represents an
binomial distribution"""


class Binomial:
    """Class that represents an binomial distribution"""
    e = 2.7182818285
    pi = 3.1415926536

    def __init__(self, data=None, n=1, p=0.5):
        if data is None:
            if n < 0:
                raise ValueError("n must be a positive value")
            if 0 <= p and p <= 1:
                self.n = int(n)
                self.p = float(p)
            else:
                raise ValueError("p must be greater than 0 and less than 1")

        else:
            if type(data) is not list:
                raise TypeError("data must be a list")
            if len(data) < 2:
                raise ValueError("data must contain multiple values")

            mean = sum(data)/len(data)
            variance = sum([(x - mean) ** 2 for x in data]) / len(data)

            p = 1 - (variance/mean)
            self.n = round(mean/p)
            self.p = mean/self.n
