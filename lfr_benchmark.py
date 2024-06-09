import networkx as nx
from networkx.generators.community import LFR_benchmark_graph
import itertools

# Example of how to use the create_graph(N, k, mu, average_degree, min_communities) function
# Tough to hit what parameters to use in order for this to work
# Fortunately there is good documentation for the LFR_benchmark_graph function
# https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html

def create_graph(N: int, k: float, mu: float, average_degree: float, min_communities: int) -> nx.Graph:
    G = LFR_benchmark_graph(n=N, tau1=k, tau2=k/2, mu=mu, average_degree=average_degree, min_community = min_communities, seed=10)
    return G