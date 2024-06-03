import networkx as nx
import time
from quality_measures import average_conductance, calculate_modularity, NMI

# In the Fluid communities paper the value for k is set to be the number of communities in the ground truth
# partitioning of the graph into communities. We pass it as an argument to the fluidc function.

def fluidc(G: nx.Graph, k: int):
    start_time = time.time()

    fluidc_communities = []

    if nx.is_connected(G):
        fluidc_communities = list(nx.community.asyn_fluidc(G, k = k, seed=10))
    else:
        Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
        for component in Gcc:
            subgraph = G.subgraph(component)
            component_communities = nx.community.asyn_fluidc(subgraph, k = k, seed=10)
            fluidc_communities.extend(component_communities)

    end_time = time.time()
    execution_time = end_time - start_time

    return fluidc_communities, execution_time