# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 19:32:12 2019
Incomplete
"""
import numpy as np
import math
from scipy import integrate

def betrag(c):
    return np.sqrt(c.real**2 + c.imag**2)


def zeta(s):
    result = 0
    
    f_real = lambda x: (x - math.floor(x) )/ x**(s.real + 1)
    f_imag = lambda x: (x - math.floor(x) )/ x**(s.imag)
    
    integral_real, _ = integrate.quad(f_real, 1,7)
    integral_imag, _ = integrate.quad(f_imag, 1,7)

    result = s / (s-1) - s * complex(integral_real, integral_imag)
        
    return result


s = complex(1/2, 14.134725141734693790457251983562)
#s = complex(1/2, 5)
x = zeta(s)


print(x)
print(betrag(x))


