from numba import jit
import numpy as np

def read_pi():
    file = open("pi.txt")
    return file.read().replace("\n", " ")

@jit(nopython=True)
def position(number):
    n = str(number)
    position = pi.find(n)
    return position + 0


def find_selfreflecting():
    p = 0
    while True:
        if position(p) == p:
            yield p
        p += 1

pi = read_pi()


#for number in find_selfreflecting():
 #   print(number)



@jit
def find(pi):
    for p in range(1000000-1):
        n = str(p)
        position = pi.find(n)
        if p == position:
            print(p)

find(pi)
print("Ende")



