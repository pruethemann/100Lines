import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


np.random.seed(seed=230)

# Generate data
n = 100
size = np.random.normal(1000,1,n).reshape(-1,1)
weight = np.random.normal(0,0.1,n).reshape(-1,1)
width = np.random.normal(0,0.1,n).reshape(-1,1)

# Generate output
w = [2,500,50]
output = w[0] * size + w[1]* weight + w[2]*width + np.random.normal(0,0.5,n).reshape(-1,1)

# Combine predictors and output
data = np.concatenate((size,weight,width), axis=1)

# Standardize data: Center to 0
scaler = StandardScaler()
scaler.fit(data)

#data = scaler.transform(data)


# Train test split
x_train, x_test, y_train, y_test = train_test_split(data, output, test_size=0.2, random_state=0)

# Linear regression
linear = LinearRegression()
linear.fit(x_train, y_train)
y_linear = linear.predict(x_test)

print(f'MSE linear train: {mean_squared_error(linear.predict(x_train), y_train)}')
print(f'MSE linear test: {mean_squared_error(y_linear, y_test)}')

print(f'Coefficients: {linear.coef_}')


######
# Lasso regression
######

# Find optimal alpha penality parameter
alphas = np.arange(0.001,2,0.01)

coeff = []
mse = []

for alpha in alphas:
    lasso = Lasso(alpha=alpha,normalize=False)
    lasso.fit(x_train, y_train)
    coeff.append(lasso.coef_)
    y_lasso = lasso.predict(x_train)

plt.plot(alphas, coeff,'x')
plt.title('Lasso')
plt.xlabel('alphas')
plt.ylabel('weights')
plt.show()

######
# Find best parameter
######
lasso = Lasso(normalize=False)
parameters = {'alpha': alphas}
lasso_regressor = GridSearchCV(lasso, parameters, scoring='neg_mean_squared_error', cv=5)
lasso_regressor.fit(x_train, y_train)

optimal_alpha = lasso_regressor.best_params_['alpha']

print(f'optimal alpha: {optimal_alpha}')
lasso = Lasso(alpha=optimal_alpha,normalize=False)
lasso.fit(x_train, y_train)
print(f'\nMSE lasso train: {mean_squared_error(lasso.predict(x_train), y_train)}')
print(f'MSE lasso test: {mean_squared_error(lasso.predict(x_test), y_test)}')
print(f'Coefficients: {lasso.coef_}')
