# Question 9. The moment I learnt Python but didn't understand oscillations

import matplotlib.pyplot as plt
import numpy as np

n = 10
c1 = 0.1
c2 = 0.1
c3 = 0.3

def dx_dt(z, x):
    return 1/(1+z**n) - c1 * x

def dy_dt(x,y):
    return x - c2  * y

def dz_dt(y,z):
    return y - c3 * z

dt = 0.01
x = 0
y=1
z=2

t_end = 300
t = np.arange(0,300,dt)
size = int(t_end * 1/dt)

x = np.zeros(size)
y = np.zeros(size)
z = np.zeros(size)

y[0] = 1
z[0] = 2


for i in range(1, size-1):
    x[i+1] = x[i] + dx_dt(z[i],x[i]) * dt
    y[i+1] = y[i] + dy_dt(x[i],y[i]) * dt
    z[i+1] = z[i] + dz_dt(y[i],z[i]) * dt

#plt.plot(t,x, label='x')
plt.plot(t,y, label='y')
#plt.plot(t,z, label='z')

plt.legend()
plt.ylim([0, 4.5])
plt.ylim([0, 50])
plt.show()