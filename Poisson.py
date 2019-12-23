###
# Calculates Poisson distributions
# https://towardsdatascience.com/the-poisson-distribution-and-poisson-process-explained-4e2cb17d459
# https://www.examsolutions.net/tutorials/exam-questions-poisson-distribution/
###

import numpy as np


# An online shop sells a computer game at an everage rate of 1 per day

def poisson(k: int, lam: float) -> float:
    return np.exp(-lam) * lam ** k / np.math.factorial(k)


sum = 0
for k in range(11):
    sum += poisson(k, 7)
print(1 - sum)

print(f'Powercuts {poisson(7,3)}')

sum = 0
for k in range(4):
    sum += poisson(k, 3)

print(f'At least 4 Powercuts {1-sum}')
