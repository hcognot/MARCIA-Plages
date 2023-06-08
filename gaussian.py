
import numpy as np


""" amp : log10 de l'amplitude lo10 of the amplitude
    mu  : centre de la gaussienne central value of the gaussian
    sigma: écart-type de la gaussienne - standard deviation of the gaussian """

""" gaussian function """
def gaussian (x, amp, mu, sigma ):
        return (10**amp)*  np.exp(-((x - mu)**2) / (2 * (sigma**2)))

""" soustraction of 2 gaussians"""
def diff_gaussian (x, amp0, mu0, sigma0, amp1, mu1, sigma1 ):
        return gaussian(x, amp0, mu0, sigma0)- gaussian(x, amp1, mu1, sigma1)