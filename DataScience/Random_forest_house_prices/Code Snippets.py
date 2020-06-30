# Fill in the line below: get names of columns with missing values
# isnull: Convertiert jeden Wert in True: Nan False: richtiger Wert
# any(): Aggregiert auf column Ebene. True falls ein Wert in colum Nan ist
missing_features = X_train.isnull().any()

# Extrahiert column names die nan sind. Alles ist in einer Series. Somit müssen Row index in list transfomiert werden
missing_features = missing_features[missing_features==True].index.tolist()

# Fill in the lines below: drop columns in training and validation data
reduced_X_train = X_train.drop(missing_features, axis=1)
reduced_X_valid = X_valid.drop(missing_features, axis=1)

# Check your answers
step_2.check()

print(X_train.isnull().any())


######## Imputer
from sklearn.impute import SimpleImputer

# Fill in the lines below: imputation
imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(imputer.transform(X_valid))

# Fill in the lines below: imputation removed column names; put them back
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns



############ Exclude variables
# Fill in the lines below: drop columns in training and validation data
drop_X_train = X_train.select_dtypes(exclude=['object'])


######## labelling
from sklearn.preprocessing import LabelEncoder

# Drop categorical columns that will not be encoded
label_X_train = X_train.drop(bad_label_cols, axis=1)
label_X_valid = X_valid.drop(bad_label_cols, axis=1)

# Apply label encoder
labler = LabelEncoder()

for col in good_label_cols:
    label_X_train[col] = labler.fit_transform(X_train[col])
    label_X_valid[col] = labler.transform(X_valid[col])


### Hot encoder

Solution:

# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[low_cardinality_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[low_cardinality_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)
