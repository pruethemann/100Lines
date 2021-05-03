import numpy as np
import matplotlib.pyplot as plt
size = 1000000
norm = [np.random.normal(0, 1, (size)) for i in range(10) ]

chi = []
sum = np.zeros(size)
for i in range(len(norm)):
    sum = sum + norm[i]**2
    chi.append(sum)

bin = np.arange(-3, 16, 0.2)
hist = []

for c in chi:
    h, bins = np.histogram(c, bins = bin)
    hist.append(h)


for i,h in enumerate(hist):
    plt.plot(bins[1:], h, label=i)

plt.legend()
plt.ylim(0,50000)
plt.xlim(-1, 15)
plt.show()
