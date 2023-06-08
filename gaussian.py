
import numpy as np


""" amp : log10 de l'amplitude
    mu  : centre de la gaussienne
    sigma: écart-type de la gaussienne"""

def gaussian (x, amp, mu, sigma ):
        return (10**amp)*  np.exp(-((x - mu)**2) / (2 * (sigma**2)))

# only positive values    
def bruit(sound):
    return abs(np.random.normal(size=50))*10**sound

# gaussienne bruitee
# noisy gaussian function
    
def noisyGaussian(x, amp, mu, sigma, sound ):
    return gaussian(x, amp, mu, sigma )+bruit(sound)

def diff_gaussian (x, amp0, mu0, sigma0, amp1, mu1, sigma1 ):
        return gaussian(x, amp0, mu0, sigma0)- gaussian(x, amp1, mu1, sigma1)