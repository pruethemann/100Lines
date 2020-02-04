import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# roll fair dice 1000 times and count k number of sizes. Repeat 10000
n = 1000
repeats = 10_000

dice = np.random.randint(1,7,(repeats,n))
six = np.where(dice < 6, 0, 1)
k = np.sum(six, axis = 1)
k = pd.Series(k)            # Convert to pandas series

## Wilkon: L(Theta) = (n k) * (n/k)^k * (1-n/k)^(n-k)
def liklehood2(k):
    p = k/n
    return m.factorial(n) / (m.factorial(k) * m.factorial(n-k)) * p**k * (1-p)**(n-k)

def liklehood1(k: int):
    """
    Calculate likelehood of H0: fair dice
    :param k: Number of dice rolls of 6
    :return:
    """
    p = 1/6
    return m.factorial(n) / (m.factorial(k) * m.factorial(n-k)) * p**k * (1-p)**(n-k)


def wilkon(L0, L1):
    """
    :param L0: Liklehood of H0 hypothesis
    :param L1: Liklehood of H1 hypothesis
    :return: log liklehood according to Wilkon
    """
    return 2*(np.log(L1)- np.log(L0))

L0 = k.apply(liklehood1)
L1 = k.apply(liklehood2)

# Log likelehood
LR = wilkon(L0, L1)

# Plot histogram
plt.hist(LR, bins = 50, density=True, label='simulated')

# H0: Fair dice
# H1: Unfair dice
# Reject H0 if LR > 3.84 (Chisquare p=0.05, df=1)
rejected = np.sum(np.where(LR > 3.84, 1, 0))

# plot chi square with df = 2
x = np.linspace(0,10,100)
df = 1 # degree of freedom
plt.plot(x, stats.chi2.pdf(x, df), label='predicted')

plt.xlim(0,10)
plt.legend()
plt.show()

# Bei 10000 Wiederholungen wird die H0 Hypothese tatsächlich 5%
# (Typ 1 Irrtumswahrscheinlichkeit) abgelehnt
print(f'{round(rejected/repeats*100,2)} % of all simulation have been rejected. H1 is wrongly accepted. Type I Error')
