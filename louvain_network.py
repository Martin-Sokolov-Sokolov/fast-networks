import networkx as nx
import time
from quality_measures import average_conductance, calculate_modularity, NMI

def louvain(G: nx.Graph):
    start_time = time.time()
    louvain_communities = nx.community.louvain_communities(G, seed=10)
    end_time = time.time()
    execution_time = end_time - start_time

    return louvain_communities, execution_time