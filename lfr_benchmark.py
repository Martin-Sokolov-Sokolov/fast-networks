import networkx as nx
from networkx.generators.community import LFR_benchmark_graph
import itertools



def create_graphs(Ns: list[int], ks: list[float], mus: list[float], average_degrees: list[float], min_communities: list[int]) -> list[nx.Graph]:
    graphs = []
    
    for N, k, mu, average_degree, min_community in itertools.product(Ns, ks, mus, average_degrees, min_communities):
        temp_g = create_graph(N, k, mu, average_degree, min_community)
        graphs.append(temp_g)
    
    return graphs

def create_graph(N: int, k: float, mu: float, average_degree: float, min_communities: int) -> nx.Graph:
    return LFR_benchmark_graph(n=N, tau1=k, tau2=k/2, mu=mu, average_degree=average_degree, min_community = min_communities, seed=10)