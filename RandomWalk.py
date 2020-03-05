import numpy as np
import matplotlib.pyplot as plt

n_steps = 100           # Number of dice flips per walk
n_walks = 1_000_000     # Number of simulated walks

# Create a n_walks x n_steps random array with either -1 / 1 entries
x = np.random.randint(0, 2, (n_walks, n_steps))
x[x==0] = -1

# Emperical Data
endpoints = np.sum(x, axis=1)   # calculate endpoints for n_walks
plt.hist(endpoints, bins=n_steps, density=True, range=(-n_steps, n_steps), label ='Emperical')

# Theoretical data: Derived from diffusion equation
mean, var = 0, n_steps

def gauss(x):
        return 1/np.sqrt(2*np.pi*var) * np.exp(-(x-mean)**2 / (2*var))

steps = np.arange(-n_steps,n_steps,0.1)
prob = gauss(steps)

plt.plot(steps, prob, color='black', label = 'Theoretical')
plt.xlabel('Distance')
plt.ylabel('Probability to reach distance')
plt.title('Random Walk in 1D')
plt.legend()
plt.show()