from lfr_benchmark import create_graph
from louvain_network import louvain
from fluid_communities import fluidc
from quality_measures import average_conductance, calculate_modularity, NMI
from helper_functions import community_to_label, ground_truth_communities

N = 250
k = 3
mu = 0.3
average_degree = 5
min_communities = 20

def main():

    # Example of how to use the create_graph(N, k, mu, average_degree, min_communities) function
    # Tough to hit what parameters to use in order for this to work
    # Fortunately there is good documentation for the LFR_benchmark_graph function
    # https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html
    graph = create_graph(N, k , mu, average_degree, min_communities)

    louvain_communities, _ = louvain(graph)
    true_communities = ground_truth_communities(graph)
    fluidc_communities, _ = fluidc(graph, len(true_communities))

    true_labels = community_to_label(true_communities, N)
    louvain_labels = community_to_label(louvain_communities, N)
    fluidc_labels = community_to_label(fluidc_communities, N)

    print("NMI for Louvain: ", NMI(true_labels, louvain_labels))
    print("NMI for Fluid communities: ", NMI(true_labels, fluidc_labels))

if __name__ == "__main__":
    main()