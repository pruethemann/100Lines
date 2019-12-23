########################
# Sierpinski (Triangle)
########################

import numpy as np
import matplotlib.pyplot as plt
import random, time

def setCorners(n):
    return [getRandomPoint() for i in range(n)]

def getRandomPoint():
    return(random.randint(0, size-1), random.randint(0, size-1))

def pickCorner():
    return points[random.randint(0,N-1)]

size = 1_000
x = np.zeros((size,size))
N = 3
factor = 2
points = setCorners(N)
points = [[size/10, size/2], [9/10*size,size/10], [9/10*size, 9/10*size]]
#points = [[200, 100], [20, 500],[200, 900],[9/10*size,size/10], [9/10*size, 9/10*size]]
print(points)

(x1,y1) = getRandomPoint()
x[x1][y1] = 1
for i in range(500_000):
    corner = pickCorner()
    (x2, y2) = (corner[0], corner[1])
    (dx, dy) = (x2 - x1, y2 - y1)

    x1 = int(x1 + dx/factor)
    y1 = int(y1 + dy/factor)

    x[x1][y1] = 1

    if i%1000==0 and i<10_000:
        plt.imshow(x, cmap='gray')
        plt.show()
        time.sleep(1)

time.sleep(1)
plt.imshow(x,cmap='gray')
plt.show()