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

N = 250
y = 3
mu_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
average_degree = 8
min_communities = 10

def main():
    run(mu_values, N, y, average_degree, min_communities)

if __name__ == "__main__":
    main()