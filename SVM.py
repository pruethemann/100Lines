import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(23)
n = 100
mean_height = {'netherlands': 175.6, 'laos': 155.9, 'switzerland': 171.0}
std_height = {'netherlands': 5.0, 'laos': 8.0, 'switzerland': 3.0}
countries = ['netherlands','laos', 'switzerland']

height_netherlands = np.random.normal(mean_height['netherlands'], std_height['netherlands'], n).reshape(-1,1)
height_laos = np.random.normal(mean_height['laos'], std_height['laos'], n).reshape(-1,1)
height_switzerland = np.random.normal(mean_height['switzerland'], std_height['switzerland'], n).reshape(-1,1)

heights = np.concatenate((height_netherlands, height_laos, height_switzerland), axis=1)

heights = pd.DataFrame(heights, columns=countries)