# Gradient Descent

import numpy as np
import matplotlib.pyplot as  plt

# Generate data

def f(x: np.ndarray) -> np.ndarray:
    """
    Function values over range x
    """
    return 3* x**2  + 10


def display_line(x,y,  i: int):
    #x = np.arange(-5,5,0.1)
    plt.scatter(x,y)


def gradient(x:  float) -> np.ndarray:
    """
    w[0] = slope
    w[1] = intercept
    """
    gradient = 6 * x
    return gradient

def gradient_step(learning_rate:float, x: float) -> float:
    """
    Computes the step size
    """
    #print(gradient(x))

    x = x - learning_rate * gradient(x)
    return x

x =  np.arange(-5,5,0.1)


plt.plot(x,f(x))


# 1. Initiate slope
slope = 10
intercept = 5
x = -10
w = np.array([slope, intercept])
x = np.array([x,-x])

display_line(-10,-10, 0)

# Start optimisation
learning_rate = 0.1

for i in range(1,50):
    x = gradient_step(learning_rate,x)
    y = f(x)
    print(x,y)

    display_line(x,y, i)

plt.legend()
plt.show()