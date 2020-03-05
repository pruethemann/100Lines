import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

from mpl_toolkits.mplot3d import Axes3D

# Example of mu and sigma in 2 dimensions
mu = np.array([-3000,10])
sigma = np.array([[4,1],[1,1]])

def gauss(x: np.ndarray) -> np.ndarray:
    """
    Calculates multivariate gaussian in 2 dimensions
    :param x: column vector of multi-dimensional point
    :return: column vector of proability a specific point x
    """
    det = np.linalg.det(sigma)
    sigma_inv = np.linalg.inv(sigma)
    return 1 / np.sqrt((2 * np.pi * det)) * np.exp( -0.5* (x-mu).T @ sigma_inv @ (x-mu))


def gauss_3D(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Calculates multivariate gaussian in d dimensions
    :param x: column vector of multi-dimensional point
    :return: column vector of proability a specific point x
    """
    det = np.linalg.det(sigma)
    sigma_inv = np.linalg.inv(sigma)
    return 1 / np.sqrt((2 * np.pi * det)) * np.expm1( -0.5* (x-0).T @ sigma_inv @ (x-0))

def gauss2D(x: np.ndarray) -> float:
    """
    Computes uni-variate gaussian
    :param x: point with 2 dimension
    :return: probability at point x
    """
    return 1 / np.sqrt((2 * np.pi * sigma_1D)) * np.exp( -(x-mu_1D)**2/(2*sigma_1D))

def landscape_sin(x):
    """
    Generate a sinus landscape.
    :param x:
    :return:
    """
    return np.sin(x)

def accept(x0: np.ndarray, x1: np.ndarray, f) -> bool:
    """
    Decides depending on the slope between current and new point whether move is accepted.
    Currently move is accepted in case slope is positive.
    :param x0: Current position
    :param x1: Potential new position.
    :param f: landscape function with a single point vector as argument.
    :return:
    """
    h0 = f(x0)              # Computes function value at position x0
    h1 = f(x1)              # Computes function value at position x1
 #   print(f'Vorher: {h0} Nachher: {h1}')
    # Decision function
    return h1-h0 >= 0

def go_2D() -> np.ndarray:
    """
    Randomly decides in which direction to go. Works currently only
    for 2 dimensions.
    :return: Array in 2D which defines new direction
    """
    x = random.randint(0,3)
    if x == 0:
        return np.array([1,0])
    if x == 1:
        return np.array([0,1])
    if x == 2:
        return np.array([-1,0])
    if x == 3:
        return np.array([0,-1])

def go_1D():
    """
    Randomly decides in which direction to go. Works currently only
    for 1 dimensions.
    :return: Array in 2D which defines new direction
    """
    x = random.randint(0,1)
    if x == 0:
        return -0.1
    if x == 1:
        return 0.1

coordinates = np.zeros((10000,2))

current = np.array([0,0])

current = -1.5
f = landscape_sin

for i in range(10):
    g = go_1D()

    if accept(current, current+g, f):
        current += g
        coordinates[i,:] = np.array([current, landscape_sin(current)])

x = np.arange(-2,4,0.1)

#### Example 1D: Sinus
mu_1D = 2
sigma_1D = 1
test = gauss2D(x)
plt.scatter(x,test)
plt.show()

"""
#### Example 2D: Multivariate Gauss in 2D
d = 50

x = np.linspace(-2,2,d)
y = np.linspace(-2,2,d)

points = np.concatenate((x, y))
points = points.reshape((2,d))


fig = plt.figure()
ax = plt.axes(projection="3d")

X, Y = np.meshgrid(x, y)

X, Y = np.meshgrid(x, y)
Z = gauss_3D(X, Y)

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_wireframe(X, Y, X, color='green')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
"""

from scipy.stats import multivariate_normal

d = 50
x = np.linspace(-2,2,d)
y = np.linspace(-2,2,d)

X, Y = np.meshgrid(x, y)

pos = np.empty(x.shape + (2,))
pos[:,:,0]=X
pos[:,:,1]=Y
F = multivariate_normal(mu, sigma)
Z = F.pdf()
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_wireframe(X, Y, Z, color='green')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
