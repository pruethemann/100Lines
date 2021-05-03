import matplotlib.pyplot as plt
import numpy as np



A = [[0.5, 1], [1,1], [1/16, 1/24], [-12,8]]
b = [12, 20, 1, 0]

# Exercise 1.3 a
A = [[-1,5], [1,1], [2,-1]]
b = [20,10,14]

A, b = np.array(A), np.array(b)

n = b.shape[0]
print(n)
x = np.linspace(0,30,100)
for i in range(n):
    plt.plot(x, (b[i]-A[i,0]*x) / A[i,1])

plt.xlim([0 ,30])
plt.ylim([0 ,30])

plt.show()