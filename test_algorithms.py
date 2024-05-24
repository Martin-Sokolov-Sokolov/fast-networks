import matplotlib.pyplot as plt

from louvain_network import louvain
from fluid_communities import fluidc
from quality_measures import NMI
from lfr_benchmark import create_graph
from helper_functions import community_to_label, ground_truth_communities

def calculate_average_nmi_for_mu_values(mu_values, N, k, average_degree, min_communities, runs=10):
    nmi_scores = {mu: {'Louvain': 0, 'Fluid Communities': 0} for mu in mu_values}

    for _ in range(runs):
        for mu in mu_values:
            graph = create_graph(N, k , mu, average_degree, min_communities)

            louvain_communities, _ = louvain(graph)
            true_communities = ground_truth_communities(graph)
            fluidc_communities, _ = fluidc(graph, len(true_communities))

            true_labels = community_to_label(true_communities, N)
            louvain_labels = community_to_label(louvain_communities, N)
            fluidc_labels = community_to_label(fluidc_communities, N)

            nmi_louvain = NMI(true_labels, louvain_labels)
            nmi_fluidc = NMI(true_labels, fluidc_labels)

            nmi_scores[mu]['Louvain'] += nmi_louvain
            nmi_scores[mu]['Fluid Communities'] += nmi_fluidc

    for mu in mu_values:
        nmi_scores[mu]['Louvain'] /= runs
        nmi_scores[mu]['Fluid Communities'] /= runs

    return nmi_scores

# Fixed parameter nmi_scores['mu']['Louvain'] and nmi_scores['mu']['Fluid Communities']
# If we add other algorithms, we can do so in this way
def plot_nmi_scores(nmi_scores):
    mu_values = list(nmi_scores.keys())
    nmi_louvain = [nmi_scores[mu]['Louvain'] for mu in mu_values]
    nmi_fluidc = [nmi_scores[mu]['Fluid Communities'] for mu in mu_values]

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(mu_values, nmi_louvain, label='Louvain')
    plt.scatter(mu_values, nmi_louvain, marker='^')
    plt.xlabel('Mu')
    plt.ylabel('NMI')
    plt.title('Louvain')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(mu_values, nmi_fluidc, label='Fluid Communities')
    plt.scatter(mu_values, nmi_fluidc, marker='^')
    plt.xlabel('Mu')
    plt.ylabel('NMI')
    plt.title('Fluid Communities')
    plt.legend()

    plt.tight_layout()
    plt.show()
    
def run(mu_values, N, k, average_degree, min_communities):
    nmi_scores = calculate_average_nmi_for_mu_values(mu_values, N, k, average_degree, min_communities)
    plot_nmi_scores(nmi_scores)