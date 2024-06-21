import numpy as np
import sklearn.preprocessing
from scipy.sparse import isspmatrix, dok_matrix, csc_matrix
import time
import networkx as nx
from pagerank import pagerank
import markov_clustering as mc
import math

normalization_constant = 8

def expansion(matrix, power = 2):
    if isspmatrix(matrix):
        return matrix ** power

    return np.linalg.matrix_power(matrix, power)
    
def inflation(matrix, power = 2):
    if isspmatrix(matrix):
        return matrix.power(power)

    return np.power(matrix, power)

def normalize(matrix):
    return sklearn.preprocessing.normalize(matrix, norm="l1", axis=0)

def add_start_clusters(matrix, starting_communities = None):
    if starting_communities is not None:
        for ind, val in starting_communities:
            rows = matrix[:, ind].nonzero()[0]
            for row in rows:
                matrix[row, ind] += math.exp(val) / normalization_constant
                matrix[ind, row] += math.exp(val) / normalization_constant
        
    return matrix

def add_self_loops(matrix):
    shape = matrix.shape[0]
    if isspmatrix(matrix):
        new_matrix = matrix.todok()
    else:
        new_matrix = matrix.copy()

    for i in range(shape):
        new_matrix[i, i] = 1
    
    if isspmatrix(matrix):
        return new_matrix.tocsc()

    return new_matrix

def prune(matrix, threshold = 0.001):
    if isspmatrix(matrix):
        pruned = dok_matrix(matrix.shape)
        pruned[matrix >= threshold] = matrix[matrix >= threshold]
        pruned = pruned.tocsc()
    else:
        pruned = matrix.copy()
        pruned[pruned < threshold] = 0

    num_cols = matrix.shape[1]
    row_indices = matrix.argmax(axis=0).reshape((num_cols,))
    col_indices = np.arange(num_cols)
    pruned[row_indices, col_indices] = matrix[row_indices, col_indices]

    return pruned

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
    non_attractors = set(range(A.shape[0])) - set(attractors)

    clusters = {}

    # Initially, add each attractor to its own cluster
    for attractor in attractors:
        clusters[attractor] = [attractor]


    # Assign each non-attractor to the cluster of the attractor with the highest connection value
    for non_attractor in non_attractors:
        col = A.getcol(non_attractor).toarray()
        # Find the attractor with the highest value for this non-attractor
        highest_attractor = np.argmax(col)
        if highest_attractor in clusters:
            clusters[highest_attractor].append(non_attractor)
        else:
            clusters[highest_attractor] = [non_attractor]

    # Convert clusters dictionary to a sorted list of tuples
    return sorted([tuple(cluster) for cluster in clusters.values()])


def mcl(A, expansion_power = 2, inflation_power = 2, threshold = 1e-6, iterations = 100
                              , pruning_threshold = 0.01, pruning_frequency = 1, starting_communities = None):

    if not isspmatrix(A):
        A = csc_matrix(A)

    A = add_self_loops(A)
    A = normalize(A)
    A = add_start_clusters(A, starting_communities)
    for i in range(iterations):
        last_A = A.copy()
        A = iterate(A, expansion_power, inflation_power)
        if (i + 1) % pruning_frequency == 0:
            A = prune(A, pruning_threshold)

        if converged(A, last_A, threshold):
            break

    return A

def execute_mcl(G, num_communities, expansion_power = 2, inflation_power = 2, threshold = 1e-6
                                                       , iterations = 100, pruning_threshold = 0.001, pruning_frequency = 1):
    A = nx.to_numpy_array(G)
    starting_communities = get_starting_clusters(G, num_communities)
    start_time = time.time()
    result = mcl(A, expansion_power, inflation_power, threshold, iterations
                                   , pruning_threshold, pruning_frequency, starting_communities)
    end_time = time.time()
    clusters = get_clusters(result)
    execution_time = end_time - start_time
    return clusters, execution_time

def original_mcl(G):
    A = nx.to_numpy_array(G)
    time_start = time.time()
    result = mc.run_mcl(A)
    clusters = mc.get_clusters(result)
    end_time = time.time()
    execution_time = end_time - time_start
    
    return clusters, execution_time
#
#A = np.array([
#    [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
#    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
#    [0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
#    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
#    [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0],
#    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
#    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
#    [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
#    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
#])
#
#G = nx.from_numpy_array(A)
#sc = get_starting_clusters(G, 3)
#clusters, execution_time = execute_mcl(G, 3)
#print(clusters, execution_time)