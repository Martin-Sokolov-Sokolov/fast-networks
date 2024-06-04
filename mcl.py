import numpy as np
import sklearn.preprocessing
from scipy.sparse import isspmatrix, dok_matrix, csc_matrix
import markov_clustering as mc

def expansion(A, power = 2):
    if isspmatrix(A):
        return A ** power
    return np.linalg.matrix_power(A, power)
    
def inflation(A, power = 2):
    if isspmatrix(A):
        return A.power(power)
    
    return np.power(A, power)

def normalize(A):
    return sklearn.preprocessing.normalize(A, norm="l1", axis = 0)

def add_self_loops(A):
    return A + np.eye(A.shape[0])

def prune(A, threshold = 1e-6):
    return normalize(np.where(A < threshold, 0, A))

# One iteration is expansion followed by inflation and normalization
# So normalize . inflation . expansion . A
def iterate(A, expansion_power, inflation_power):
    return normalize(inflation(expansion(A, expansion_power), inflation_power))

def converged(A, B, threshold = 0.1):
    return np.linalg.norm(A - B) < threshold

def get_clusters(A):

    if not isspmatrix(A):
        A = csc_matrix(A)

    attractors = A.diagonal().nonzero()[0]

    clusters = set()

    for attractor in attractors:
        cluster = tuple(A.getrow(attractor).nonzero()[1].tolist())
        clusters.add(cluster)

    return sorted(list(clusters))

def mcl(A, expansion_power = 2, inflation_power = 2, threshold = 0.1, iterations = 100):
    A = add_self_loops(A)
    A = normalize(A)
    B = iterate(A, expansion_power, inflation_power)
    for i in range(iterations):
        A = B
        B = iterate(A, expansion_power, inflation_power)
    return B

A = np.array([
    [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
])

result = mcl(A)
clusters = get_clusters(result)
print(clusters)