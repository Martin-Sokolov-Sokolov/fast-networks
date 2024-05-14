import networkx as nx
from networkx.generators.community import LFR_benchmark_graph
import itertools

Ns = [250, 3000, 40000]
ks = [2, 3, 4]
mus = [0.1, 0.3, 0.5]
average_degrees = [2, 3, 4]
min_communities = [3, 7, 10]


# TODO FIX THIS
def create_graphs(Ns: list[int], ks: list[float], mus: list[float], average_degrees: list[float], min_communities: list[float]) -> list[nx.Graph]:
    graphs = []
    
    for N, k, mu, average_degree, min_community in itertools.product(Ns, ks, mus, average_degrees, min_communities):
        temp_g = LFR_benchmark_graph(n=N, tau1=k, tau2=k, mu=mu, average_degree=average_degree, min_community=min_community, seed=123)
        graphs.append(temp_g)
    
    return graphs

def create_graph(N: int, k: float, mu: float, average_degree: float, min_communities: int) -> nx.Graph:
    return LFR_benchmark_graph(n=N, tau1=k, tau2=k/2, mu=mu, average_degree=average_degree, min_community = min_communities, seed=10)