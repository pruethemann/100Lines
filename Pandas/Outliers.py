import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

size=200

np.random.seed(2)

x = np.random.randint(1,100,(100))
x = np.arange(0,100)

s1 = pd.Series(x)
s2 = s1[s1.between(s1.quantile(.05), s1.quantile(.95))] # without outliers



df = pd.DataFrame(np.random.randint(10,90,size=(1000, 2)), columns=list('AB'))
df['AO'] = df.A
df['BO'] = df.B
schablone = df.A.between(df.A.quantile(.05), df.A.quantile(.95))

df.AO = df.A[schablone]
df.BO = df.B[df.B.between(df.B.quantile(.15), df.B.quantile(.85))]


df.boxplot(column=['A','AO','B','BO'])

x = np.array([1,3,4,5,6])
y = np.array([True, False, False, True, True])

x = pd.Series(x)
y = pd.Series(y)

a = x[y]
print(a)

x = np.arange(1,11)
x = pd.Series(x)
print(x.quantile(0.25))
print(x.between(3,5))




plt.show()
