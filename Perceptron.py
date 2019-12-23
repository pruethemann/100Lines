import numpy as np
import matplotlib.pyplot as plt

x = np.array([-7., -11., -10., -12., 5., 4.,6., 3.])
y = np.array([12.,10.,9.,9.,       5.,3., 3., -5.])
z = np.zeros(8)

label = np.array([-1, -1, -1, -1, 1, 1, 1, 1])

X = np.vstack((x,y,z))

w0 = np.array([1.,1.,-.5])
w = np.array([1.,1.,-.5])

x_axis = np.array([-12., 12.])
y_axis = np.zeros(2)

nu = 0.2
for iter in range(2):
    for i in range(8):
       # print(w0.T @ X[:,i], "  ", X[:,i])
        if w0.T @ X[:,i] > 0 and label[i] == -1: ## delta = 1 Sollte -1 (links sein, ist aber rechts)
            #print(X[:,i])
            w += - nu * X[:,i] * 1

        if w0.T @ X[:,i] < 0 and label[i] == 1:  ## delta = -1 Sollte 1 sein (rechts sein, ist aber links)
            #print(X[:,i])
            w += - nu * X[:, i] * -1
    for i in range(2):
        y_axis[i] = -w0[0] / w0[1] * x_axis[i] + w0[2]
    plt.plot(x_axis, y_axis, label = str(iter+1))

    w0 = w


print(w)

plt.xlim(-15, 15)
plt.ylim(-6,12)
plt.scatter(x,y)
plt.legend()
plt.show()