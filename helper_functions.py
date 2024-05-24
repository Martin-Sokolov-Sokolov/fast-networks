def community_to_label(community_list, N):
    label = [0] * N
    for i, community in enumerate(community_list):
        for node in community:
            label[node] = i
    return label

def ground_truth_communities(G):
    communities = []
    for node, data in G.nodes(data=True):
        community = data['community']
        if community not in [c[0] for c in communities]:
            communities.append((community, {node}))
        else:
            for c in communities:
                if c[0] == community:
                    c[1].add(node)
                    break
    return [c[1] for c in communities]