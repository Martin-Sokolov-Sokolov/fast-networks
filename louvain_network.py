import networkx as nx
import time
from quality_measures import average_conductance, calculate_modularity, NMI

path_to_networks = "../"
G = nx.read_edgelist(path_to_networks + "protein.edgelist.txt", delimiter='\t', create_using=nx.Graph())

#G = nx.Graph()
#G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (6, 7), (7, 8), (8, 9)])

def louvain(G: nx.Graph):
    start_time = time.time()
    louvain_communities = nx.community.louvain_communities(G, seed=123)
    end_time = time.time()
    execution_time = end_time - start_time

    return louvain_communities, execution_time

communities, exec_time = louvain(G)
modularity = calculate_modularity(G, communities)
conductance = average_conductance(G, communities)

# Calculate NMI for the SAME algorithm, but for different paramters (like mu)
# In this case it is 1 as we are using the same communities for the test
# Which means there is a perfect correlation between the ground truth and the guessed communities
# We can use this later when we introduce different parameters for the same algorithm
nmi = NMI(communities, communities)

print("Number of communities: ", len(communities))
print("Modularity: ", modularity)
print("Execution time: ", exec_time, " seconds")
print("Average conductance: ", conductance)
print(nmi)