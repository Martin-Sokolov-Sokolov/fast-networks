from lfr_benchmark import create_graph
from louvain_network import louvain
from fluid_communities import fluidc
from quality_measures import average_conductance, calculate_modularity, NMI
from helper_functions import community_to_label, ground_truth_communities
from test_algorithms import run

N = 250
k = 3
mu_values = [0.1, 0.2, 0.3]
average_degree = 5
min_communities = 20

def main():
    run(mu_values, N, k, average_degree, min_communities)

if __name__ == "__main__":
    main()