import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import sys

def mean_squared_error_score(n_estimators: int):
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=n_estimators, random_state=235))])
    scores = -1 * cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_absolute_error')
    return scores.mean()

X = pd.read_csv('./data/train.csv')
X_test = pd.read_csv('./data/test.csv')

# Extract House price as target
y = X.SalePrice
X.drop(['SalePrice','Id'], axis=1, inplace=True)
id = X_test.Id
X_test.drop(['Id'], axis=1, inplace=True)

# Define Preprocessing steps

# Numerical
num_transfomer = SimpleImputer(strategy='constant')

# Categorical
cat_transformer = Pipeline(steps= [
    ('imputer', SimpleImputer(strategy='constant')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))]
)

# Define categorical and numerical variables
num_vars = X.select_dtypes(include=['int64','float64']).columns
cat_vars = X.select_dtypes(include=['object']).columns
cat_vars = [cname for cname in X.columns if
                    X[cname].nunique() < 10 and
                    X[cname].dtype == "object"]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transfomer, num_vars),
        ('cat', cat_transformer, cat_vars)])

### Find optimal settings

scores = {}
for n in range(1,300,20):
    scores[n] = mean_squared_error_score(n)


n_trees, mse = np.array(list(scores.keys())), np.array(list(scores.values()))

plt.scatter(n_trees, mse)
plt.plot(n_trees, mse)

n_trees_optimal = n_trees[np.argmin(mse)]
print(f'Optimal number of trees: {n_trees_optimal}')
plt.show()


# Create pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=n_trees_optimal, random_state=235))])


pipeline.fit(X, y)
y_predict = pipeline.predict(X_test)

#Save test predictions to file
output = pd.DataFrame({'Id': id,
                       'SalePrice': y_predict})
output.to_csv(f'HousePrices_{n_trees_optimal}.csv', index=False)
