import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def draw_samples(dist, n, size):
    """
    Randomly pick n samples from a distribution and compute mean.
    :param dist: Distribution
    :param n: How often are samples drawn and mean determined
    :param size: How many samples should be drawn in one go
    :return: array with n means for every drawn step
    """
    means = np.zeros(n)
    for i in range(n):
        # Sample "size" samples from dist
        samples = np.random.choice(exp, size)
        means[i] = np.mean(samples)

    return means

# Create a exponential distribution
exp = np.random.exponential(.1, 1000000)


# Sample 100x 100 samples from distr
samples_exp = draw_samples(exp, 1000, 1000)

# Plotting
plt.subplot(2,1,1)
sns.distplot(exp)
plt.title("Exponential Dist")
plt.subplot(2,1,2)
sns.distplot(samples_exp)
plt.title("CLT")
plt.show()
