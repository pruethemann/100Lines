import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def multivariate_normal(n: int, mu: float, sigma: float) -> np.ndarray:
    
    x,y = np.random.multivariate_normal(mu, sigma, n).T
    return (x,y)

def generate_date(n: int, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    
    x1, y1 = multivariate_normal(n, mu[0], sigma[0])
    x2, y2 = multivariate_normal(n, mu[1], sigma[1])

    x = np.concatenate((x1, x2)).reshape((-1,1))
    y = np.concatenate((y1, y2)).reshape((-1,1))

    X = np.concatenate((x,y), axis = 1)
    return X



def plot(X: np.ndarray, labels: np.ndarray, center1, center2, iter):

    plt.scatter(X[ : , 0], X[ :, 1], c=labels)
    plt.scatter(center1[0], center1[1], c='k', marker='x',)
    plt.scatter(center2[0], center2[1], c='k', marker='x',)

    plt.title(f'Iteration: {iter}')
    plt.show()
    plt.pause(0.5)

def k_means(n_clusters: int, x: np.ndarray):
    Kmean = KMeans(n_clusters)

    Kmean.fit(X)

    center = Kmean.cluster_centers_

    labels = Kmean.labels_

    return labels

def calc_distance(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def k_means_(n_clusters, X, n):
    # Random define center
    c1 = [-10, 12.5]
    c2 = [10, 0]
    labels = np.zeros(n)

    eps = 1
    iter = 1
    max_iter = 100

    while eps > 0.01 or iter > max_iter:
        plot(X, labels, c1, c2, iter)


        # Expecation step: Assigns point to cluster
        for i in range(n):
            if calc_distance(X[i , :], c1) > calc_distance(X[i , :], c2):
                labels[i] = 1
            else:
                labels[i] = 0

        # Maximsation step: Calculate new center
        c1_new = np.mean(X[labels == 0], axis=0)
        c2 = np.mean(X[labels == 1], axis=0)

        # Breaking condition
        eps = abs(np.sum(c1_new - c1))
        c1 = c1_new
        iter += 1

    return (c1, c2)


n = 100

mu = [[10,10], [-2,3]]
#mu = [[10,10], [8,8]]
sigma =[ [[2,0],[0,2]] , [[5,0],[0,2]] ]

X = generate_date(n, mu, sigma)


n_clusters = 2
labels = k_means(n_clusters, X)
(center1, center2) = k_means_(n_clusters, X, 2*n)

print(f'Center1: {center1}')
print(center2)









