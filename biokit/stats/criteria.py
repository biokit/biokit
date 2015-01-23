import math


def AIC(L, k):
    return 2*k - 2 * math.log(L)


def AICc(L, k, n):
    return AIC(L, k) + 2*k*(k+1.)/(n-k-1.)


def BIC(L, k, n):
    return -2 * math.log(L) + k * (math.log(n) - math.log(2*math.pi))

