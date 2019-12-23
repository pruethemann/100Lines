# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 22:23:16 2019

@author: peter
"""

import numpy as np
import matplotlib.pyplot as pl

n = 10
c1 = c2 = c3 = 0.1

t = 0
x = 0
y = 1
z = 2

xp = np.zeros(500)
yp = np.zeros(500)
zp = np.zeros(500)
tp = np.zeros(500)

t_end = 500
dt = 5

for dt in range(t, t_end):
    dx = 1/(1+z**n) - c1 * x
    dy = x - c2 * y
    dz = y - c3 * z
    
    x += dx
    y += dy
    z += dz
    xp[dt] = x
    yp[dt] = y
    zp[dt] = z
    tp[dt] = dt
    
print(xp[0:10])

pl.plot(zp)
pl.plot(xp)
pl.plot(yp)
pl.show()