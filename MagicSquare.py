import numpy as np


for i in range(10000000):
    x = np.random.randint(1, 100000, (3, 3))
    q = x ** 2

    if np.array_equal(np.sum(q, axis=1),  np.sum(q, axis=0)):
        print(np.sum(q, axis=1), np.sum(q, axis=0))
        print(q)


