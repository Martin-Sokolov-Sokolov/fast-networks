import networkx as nx
import time
from quality_measures import average_conductance, calculate_modularity, NMI
import math

path_to_networks = "../"
G = nx.read_edgelist(path_to_networks + "protein.edgelist.txt", delimiter='\t', create_using=nx.Graph())

#G = nx.Graph()
#G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7), (7, 8), (8, 9)])

# In the Fluid communities paper a value of 1/10 of the number of nodes
# is used as the parameter for maxumum number of nodes in a community

def fluidc(G: nx.Graph):
    start_time = time.time()

    fluidc_communities = []

    if nx.is_connected(G):
        num_nodes = G.number_of_nodes()
        fluidc_communities = nx.community.asyn_fluidc(G, k = math.ceil(num_nodes / 10), seed=123)
    else:
        Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
        for component in Gcc:
            subgraph = G.subgraph(component)
            num_nodes_subgraph = subgraph.number_of_nodes()

            # Play around with the parameter k
            # for value num_nodes_subgraph / 100 it is close to the louvain algorithm
            component_communities = nx.community.asyn_fluidc(subgraph, k = math.ceil(num_nodes_subgraph / 10), seed=123)
            
            fluidc_communities.extend(component_communities)

    end_time = time.time()
    execution_time = end_time - start_time

    return fluidc_communities, execution_time

communities, exec_time = fluidc(G)
modularity = calculate_modularity(G, communities)
conductance = average_conductance(G, communities)
nmi = NMI(communities, communities)

print("Number of communities: ", len(communities))
print("Modularity: ", modularity)
print("Execution time: ", exec_time, " seconds")
print("Average conductance: ", conductance)
print(nmi)
