import numpy as np
import pandas as pd
#import Bio
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

# https://people.revoledu.com/kardi/tutorial/Clustering/Numerical%20Example.htm

np.random.seed(5)

# Generate data
size = 6
x = np.random.randint(0,10,(size,2))

# Calculate distance matrix
def euclidian_distance(x1,x2):
    return np.sqrt((x2[0] - x1[0])**2 + (x2[1] - x1[1])**2)

d = np.zeros((size,size))

for i in range(size):
    for j in range(size):
        d[i,j] = euclidian_distance(x[i,:],x[j,:])

#d = pd.read_csv('clusters.txt', index_col='index')
d = pd.read_csv('HierarchicalClustering/JC69.txt', index_col='index')
d = np.array(d)
d = np.triu(d)

clusters = ['A','B','C','D','E','F']
clusters = ['O','G','C','H']
size = len(d)
tree = {}

def single_linkage(x1,x2):
    return min(x1, x2)

def UMPGA(x1,x2,n1,n2):
    return (n1*x1 + n2*x2) / (n1+n2)

# Start Cluster algorithm

# 2. Single Linkage
n = 1
for n in range(1,size):

    # 1. Find smallest distance
    union = np.where(d == d[d > 0].min())
    union = [union[0][0], union[1][0]]
    union_distance = np.min(d[d > 0])
    print(f'Union: {union} Distance {union_distance}')
    print(d,'\n')

    # save distance in tree
    u1, u2 = union[0], union[1]
    tree[clusters[u1] + clusters[u2]] = union_distance / 2

    # Merge union
    untouched = [i for i in np.arange(size-n) if i not in union]

    for u in untouched:
        linkage = single_linkage(d[u,u1], d[u,u2])
        n1 = len(clusters[u1])
        n2 = len(clusters[u2])
        umpga = UMPGA(d[u,u1], d[u,u2],n1,n2)
        d[u, union[0]] = umpga

    # Save created union
    clusters[u1] = clusters[u1] + clusters[u2]

    # removed unsued
    d[:,u2] = 0


print(f'Tree: {tree}')
print(clusters)

#tree = bio.phylo.parse('phyloxml_examples.xml', 'phyloxml').next()
#print(tree)