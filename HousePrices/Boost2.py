# %% My first Machine Learning project
# Import Data
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import sys

X = pd.read_csv('./data/train.csv')
X_test = pd.read_csv('./data/test.csv')

# Extract House price as target
y = X.SalePrice
X.drop(['SalePrice'], axis=1, inplace=True)

# Split data into training and validation set
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

id_test = X_test['Id']
X_train.drop(['Id'], inplace=True, axis=1)
X_test.drop(['Id'], inplace=True, axis=1)
X_valid.drop(['Id'], inplace=True, axis=1)

# %% Handle missing Nan values
### TODO differentiate high variable and low variable missing values
# Extract all categorical data
cat_vars_train = X_train.select_dtypes(include=['object'])

# Find columns with missing data
cat_vars_train = cat_vars_train.isnull().any()
cat_vars_train = cat_vars_train[cat_vars_train == True].index

# Extract all categorical data
cat_vars_test = X_test.select_dtypes(include=['object'])

# Find columns with missing data
cat_vars_test = cat_vars_test.isnull().any()
cat_vars_test = cat_vars_test[cat_vars_test == True].index

cat_vars = set(cat_vars_train).union(tuple(cat_vars_test))

# Extract all numerical data from train
num_vars = X_train.select_dtypes(exclude=['object'])
num_vars = num_vars.isnull().any()
num_vars = num_vars[num_vars == True].index

# Extract all numerical data from test
num_vars_test = X_test.select_dtypes(exclude=['object'])
num_vars_test = num_vars_test.isnull().any()
num_vars_test = num_vars_test[num_vars_test == True].index

num_vars = set(num_vars).union(tuple(num_vars_test))

# Create an Imputer to replace Nan values
imputer_cat = SimpleImputer(strategy='most_frequent')
imputer_num = SimpleImputer(strategy='mean')

# Replace missing categorical and numerical values with Imputer
X_train_cat = pd.DataFrame(imputer_cat.fit_transform(X_train[cat_vars]), columns=cat_vars)
X_train_num = pd.DataFrame(imputer_num.fit_transform(X_train[num_vars]), columns=num_vars)

# Transform same settings to validation and test set
X_valid_cat = pd.DataFrame(imputer_cat.transform(X_valid[cat_vars]), columns=cat_vars)
X_valid_num = pd.DataFrame(imputer_num.transform(X_valid[num_vars]), columns=num_vars)
X_test_cat = pd.DataFrame(imputer_cat.transform(X_test[cat_vars]), columns=cat_vars)
X_test_num = pd.DataFrame(imputer_num.transform(X_test[num_vars]), columns=num_vars)

# Merge numerical and categorical datasets together
X_train.drop(num_vars, axis=1, inplace=True)
X_train.drop(cat_vars, axis=1, inplace=True)
X_train.reset_index(drop=True, inplace=True)
X_train = pd.concat([X_train, X_train_num, X_train_cat], axis=1)

X_valid.drop(num_vars, axis=1, inplace=True)
X_valid.drop(cat_vars, axis=1, inplace=True)
X_valid.reset_index(drop=True, inplace=True)
X_valid = pd.concat([X_valid, X_valid_num, X_valid_cat], axis=1)

X_test.drop(num_vars, axis=1, inplace=True)
X_test.drop(cat_vars, axis=1, inplace=True)
X_test.reset_index(drop=True, inplace=True)
X_test = pd.concat([X_test, X_test_num, X_test_cat], axis=1)

# %% Encode categorical variables

label_vars = X_train.select_dtypes(include=['object']).columns

# find all unique labels
cardinality = X_train[label_vars].nunique()
# Ignore / Drop all values with more than 5 labels
# X_train.drop(cardinality[cardinality >= 10].index, axis=1, inplace=True)

# Initate Labler

labler = LabelEncoder()

# Label encode

# Columns that can be safely label encoded
good_label_cols = [col for col in label_vars if
                   set(X_train[col]) == set(X_valid[col])]

# Problematic columns that will be dropped from the dataset
bad_label_cols = list(set(label_vars) - set(good_label_cols))

# Drop bad labels
X_train.drop(bad_label_cols, axis=1, inplace=True)
X_valid.drop(bad_label_cols, axis=1, inplace=True)
X_test.drop(bad_label_cols, axis=1, inplace=True)

for var in good_label_cols:
    X_train[var] = labler.fit_transform(X_train[var])
    X_valid[var] = labler.transform(X_valid[var])
    X_test[var] = labler.fit_transform(X_test[var])

# %% Training and Prediction

model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
model.fit(X_train, y_train, early_stopping_rounds=5, eval_set=[(X_valid, y_valid)])
y_predict = model.predict(X_valid)

print(mean_squared_error(y_valid, y_predict))
print(mean_absolute_error(y_valid, y_predict))


# %% Full power
data = X_train.append(X_valid)
y = y_train.append(y_valid)

model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
model.fit(data, y)
y_predict = model.predict(X_test)

# Save test predictions to file
output = pd.DataFrame({'Id': id_test,
                       'SalePrice': y_predict})
output.to_csv('XGBboost.csv', index=False)

print("You fucking did it")



