import numpy as np
import sklearn.preprocessing
from scipy.sparse import isspmatrix, dok_matrix, csc_matrix
import time
import networkx as nx
from pagerank import pagerank

def expansion(A, power = 2):
    return A ** power
    
def inflation(A, power = 2):
    return A.power(power)

def normalize(A):
    column_sums = A.sum(axis = 0)
    return A / column_sums

def add_self_loops(A, starting_communities = None):
    A = A.tolil()
    A.setdiag(1)
    if starting_communities is not None:
        for index, value in starting_communities:
            A[index, index] += value
    return A.tocsr()

def prune(A, pruning = 0.001):
    return A.multiply(A >= pruning)

# One iteration is expansion followed by inflation and normalization
# So normalize . inflation . expansion . A
def iterate(A, expansion_power, inflation_power):
    return normalize(inflation(expansion(A, expansion_power), inflation_power))

def sparse_allclose(a, b, rtol=1e-5, threshold=1e-6):
    c = np.abs(a - b) - rtol * np.abs(b)
    return c.max() <= threshold

def converged(A, B, threshold = 1e-6):
    return sparse_allclose(A, B, threshold)

def get_starting_clusters(G, num_communities):
    return pagerank(G, num_communities)

def get_clusters(A):
    if not isspmatrix(A):
        A = csc_matrix(A)

    attractors = A.diagonal().nonzero()[0]

    clusters = set()

    for attractor in attractors:
        cluster = tuple(A.getrow(attractor).nonzero()[1].tolist())
        clusters.add(cluster)

    return sorted(list(clusters))


def mcl(A, expansion_power = 2, inflation_power = 2, threshold = 1e-6, iterations = 100
                              , pruning_threshold = 0.001, pruning_frequency = 6, starting_communities = None):

    if not isspmatrix(A):
        A = csc_matrix(A)

    A = add_self_loops(A, starting_communities)
    A = normalize(A)

    for i in range(iterations):
        last_A = A.copy()
        A = iterate(A, expansion_power, inflation_power)
        if (i + 1) % pruning_frequency == 0:
            A = prune(A, pruning_threshold)

        if converged(A, last_A, threshold):
            break

    return A

def execute_mcl(G, num_communities, expansion_power = 2, inflation_power = 2, threshold = 1e-6
                                                       , iterations = 100, pruning_threshold = 0.001, pruning_frequency = 6):
    A = nx.to_numpy_array(G)
    start_time = time.time()
    starting_communities = get_starting_clusters(G, num_communities)
    result = mcl(A, expansion_power, inflation_power, threshold, iterations
                                   , pruning_threshold, pruning_frequency, starting_communities)
    end_time = time.time()
    clusters = get_clusters(result)
    execution_time = end_time - start_time
    return clusters, execution_time

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

G = nx.from_numpy_array(A)
sc = get_starting_clusters(G, 3)
clusters, execution_time = execute_mcl(G, 3)
print(clusters)