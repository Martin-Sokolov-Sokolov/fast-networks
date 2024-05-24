import networkx as nx
from sklearn.metrics.cluster import normalized_mutual_info_score

def calculate_modularity(graph, communities):
    modularity = nx.algorithms.community.modularity(graph, communities)

    return modularity

def average_conductance(G: nx.Graph, communities):
    conductance_values = [nx.algorithms.cuts.conductance(G, community) for community in communities]
    return sum(conductance_values) / len(conductance_values)


def NMI(labels_true, labels_pred):
    nmi = normalized_mutual_info_score(labels_true, labels_pred)
    return nmi