import numpy as np
from sklearn.impute import SimpleImputer

data = [[1, 2], [np.nan, 3], [7, 6]]
inputer = SimpleImputer(missing_values=np.nan, strategy='mean')
inputer.fit(data)
SimpleImputer()

print(inputer.transform(data))
