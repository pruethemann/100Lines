import time
import numpy as np

def square(x):
    return x**2

l = [x for x in range(10000)]

start = time.time()
s = list( map(square, l)   )
print(time.time()-start)


start = time.time()
lam = list( map(lambda x: x**2, l)   )
print(time.time()-start)

start = time.time()
lam = [x**2 for x in l]
print(time.time()-start)

