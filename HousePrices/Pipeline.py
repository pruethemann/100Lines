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
import sys


X = pd.read_csv('./data/train.csv')
X_test = pd.read_csv('./data/test.csv')

# Extract House price as target
y = X.SalePrice
X.drop(['SalePrice','Id'], axis=1, inplace=True)
id = X_test.Id
X_test.drop(['Id'], axis=1, inplace=True)

# Split data into training and validation set
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2)

# Define Preprocessing steps

# Numerical
num_transfomer = SimpleImputer(strategy='constant')

# Categorical
cat_transformer = Pipeline(steps= [
    ('imputer', SimpleImputer(strategy='constant')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))]
)

# Define categorical and numerical variables
num_vars = X_train.select_dtypes(include=['int64','float64']).columns
cat_vars = X_train.select_dtypes(include=['object']).columns
cat_vars = [cname for cname in X_train.columns if
                    X_train[cname].nunique() < 10 and
                    X_train[cname].dtype == "object"]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transfomer, num_vars),
        ('cat', cat_transformer, cat_vars)])

# Create model
model = RandomForestRegressor(n_estimators=300)

# Create pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)])

# Training
pipeline.fit(X_train, y_train)
prediction = pipeline.predict(X_valid)

# Fullpower
X = X_train.append(X_valid)
y = y_train.append(y_valid)

pipeline.fit(X_train, y_train)
y_predict = pipeline.predict(X_test)

#Save test predictions to file
output = pd.DataFrame({'Id': id,
                       'SalePrice': y_predict})
output.to_csv('Pipeline.csv', index=False)
