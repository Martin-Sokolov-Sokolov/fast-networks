import networkx as nx

# Looks absurd for now, but later if we have time we can implement
# personalized pagerank or some other heuristic to get the most favorable
# nodes to start the community detection algorithm from them
def pagerank(G: nx.Graph, num_communities: int):
    pr = nx.pagerank(G)
    sorted_pr = sorted(pr.items(), key = lambda x: x[1], reverse = True)[:num_communities]
    return sorted_pr