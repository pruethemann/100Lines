from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import sys

import pandas as pd

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

#print(test.info())

# Feature extraction for training
features = train.columns.tolist()

features = train.select_dtypes(include=['int64','float64']).columns.tolist()
categorial = train.select_dtypes(include='object').columns.tolist()


# Hot encoding: Categorical to Numeric

df = pd.get_dummies( columns = categorial, data=train )


print(train['SaleCondition_Normal'])
print(df['SaleCondition_Normal'])
#print(train.info())

sys.exit()

features = features.columns.tolist()

features = train.columns.tolist()
train = train[features]

train = train.interpolate()

y = train.SalePrice
features.remove('SalePrice')
features.remove('Id')
X = train[features]



# Train model
model = RandomForestRegressor(random_state=0)
model.fit(X,y)

# Feature extraction for testing
features.append('Id')
test_X = test[features]


test_X = test_X.interpolate()

index = test_X.Id
index = index.reset_index()

features.remove('Id')

prediction = model.predict(test_X[features])


prediction = pd.Series(prediction)
prediction.name = "SalePrice"

result = prediction.to_frame().join(index)
result.Id = round(result.Id,0)
result.index = result.Id



result['SalePrice'].to_csv('export.csv')

# Assess error
#print(mean_squared_error(prediction, test_y))

