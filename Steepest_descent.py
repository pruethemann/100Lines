# Homework 2 of Molecular Modeling
# Task 2:

"""
2.	[4 pts] Two particles in one dimension (only x-axis) interact with the following potential (neglect any units):
with Δx12 = distance between particles 1 and 2.
The initial positions for the two particles are x1=0 and x2=4.
Energy minimization using the steepest descent algorithm is performed with fixed step size of F (F = force on particle).
Please compute the positions and relative distance between the two particles for 10 steps of minimization, for each of the following fixed step sizes:

The single bond interactions is defined as:

V = 1/2 *( d - 2)**2

distance d = x2-x1

a.	0.1·F
b.	0.5·F
c.	1.1·F
"""

import numpy as np
import matplotlib.pyplot as plt

# Set up

steps = 10
s = np.arange(1,steps+1)



# Calculate the Gradient (Derivative to x1 and x2)
# d/dx1 = x1-x2+2
# d/dx2 = x2-x1-2

# Steppest gradient
# x(k+1) = x(k) - per_step * gradient(x(k))

per_step = [0.1,0.5,1.1]

for step in per_step:
    x1 = np.zeros(steps)
    x2 = np.zeros(steps)
    x2[0] = 4

    for i in range(1, steps):
        x1[i] = x1[i-1] - step * (x1[i-1] - x2[i-1] + 2)
        x2[i] = x2[i-1] - step * (x2[i-1] - x1[i-1] - 2)

    plt.plot(s, x2-x1, label=str(step))
    plt.legend()
    plt.show()