from lfr_benchmark import create_graph
from louvain_network import louvain
from fluid_communities import fluidc
from quality_measures import average_conductance, calculate_modularity, NMI
from helper_functions import community_to_label, ground_truth_communities
from test_algorithms import run, plot
from mcl import execute_mcl
import numpy as np
import networkx as nx
import markov_clustering as mc
import random
import time

N = 2000
k = 3
mu_values = [0.1, 0.2, 0.3]
average_degree = 4
min_communities = 200

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

def main():
    run(mu_values, N, k, average_degree, min_communities)

if __name__ == "__main__":
    main()