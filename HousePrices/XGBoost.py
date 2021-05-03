import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import sys
import numpy as np

# https://www.kaggle.com/aashita/advanced-pipelines-tutorial

X = pd.read_csv('./data/train.csv')
X_test = pd.read_csv('./data/test.csv')

# Extract House price as target
y = np.log1p(X['SalePrice'])
X.drop(['SalePrice','Id'], axis=1, inplace=True)
id = X_test.Id
X_test.drop(['Id'], axis=1, inplace=True)

# Split data into training and validation set
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2)

# Define Preprocessing steps

# Numerical
num_transfomer = SimpleImputer(strategy='mean')

# Categorical
cat_transformer = Pipeline(steps= [
    ('imputer', SimpleImputer(strategy='most_frequent')),
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


# Create pipeline

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('xgbrg', XGBRegressor())])

# defining parameters

param_grid = {
    'xgbrg__n_estimators' : [10, 50, 100, 500],
    'xgbrg__learning_rate': [0.1, 0.5, 1]}

fit_params = {"xgbrg__eval_set": [(X_valid, y_valid)],
              "xgbrg__early_stopping_rounds": 10,
              "xgbrg__verbose": False}

def optimal_learning_rate(lr):
    model = XGBRegressor(n_estimators=500, learning_rate=lr, random_state=237)
    # Create pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)])
    pipeline.fit(X_train, y_train)
    y_predict = pipeline.predict(X_valid)
    return mean_absolute_error(y_valid, y_predict)

import numpy as np
"""
maes = {}
lrs = np.linspace(0.01,0.2,num=20)

for lr in lrs:
    maes[lr] = optimal_learning_rate(lr)

plt.scatter(list(maes.keys()), list(maes.values()))
plt.plot(list(maes.keys()), list(maes.values()))
plt.show()
"""

# Validate testset
print(optimal_learning_rate(0.05))

# Predict test_set
model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
# Create pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)])
pipeline.fit(X, y)
y_predict = pipeline.predict(X_test)

#Save test predictions to file
output = pd.DataFrame({'Id': id,
                       'SalePrice': np.exp(y_predict)})
output.to_csv(f'HousePrices_XGBoost_log.csv', index=False)
