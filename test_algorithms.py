import matplotlib.pyplot as plt
import numpy as np
from louvain_network import louvain
from fluid_communities import fluidc
from mcl import execute_mcl
from quality_measures import NMI
from lfr_benchmark import create_graph
from helper_functions import community_to_label, ground_truth_communities, plot_graph

def calculate_average_nmi_for_mu_values(mu_values, N, k, average_degree, min_communities, runs=10):
    nmi_scores = {mu: {'Louvain': 0, 'Fluid Communities': 0, 'MCL': 0} for mu in mu_values}
    time_scores = {mu: {'Louvain': 0, 'Fluid Communities': 0, 'MCL': 0} for mu in mu_values}

    for _ in range(runs):
        for mu in mu_values:
            graph = create_graph(N, k , mu, average_degree, min_communities)
            
            true_communities = ground_truth_communities(graph)
            louvain_communities, louvain_time = louvain(graph)
            fluidc_communities, fluidc_time = fluidc(graph, len(true_communities))
            mcl_communities, mcl_time = execute_mcl(graph)

            true_labels = community_to_label(true_communities, N)
            louvain_labels = community_to_label(louvain_communities, N)
            fluidc_labels = community_to_label(fluidc_communities, N)
            mcl_labels = community_to_label(mcl_communities, N)

            nmi_louvain = NMI(true_labels, louvain_labels)
            nmi_fluidc = NMI(true_labels, fluidc_labels)
            nmi_mcl = NMI(true_labels, mcl_labels)

            nmi_scores[mu]['Louvain'] += nmi_louvain
            nmi_scores[mu]['Fluid Communities'] += nmi_fluidc
            nmi_scores[mu]['MCL'] += nmi_mcl

            time_scores[mu]['Louvain'] += louvain_time
            time_scores[mu]['Fluid Communities'] += fluidc_time
            time_scores[mu]['MCL'] += mcl_time

    for mu in mu_values:
        nmi_scores[mu]['Louvain'] /= runs
        nmi_scores[mu]['Fluid Communities'] /= runs
        nmi_scores[mu]['MCL'] /= runs

        time_scores[mu]['Louvain'] /= runs
        time_scores[mu]['Fluid Communities'] /= runs
        time_scores[mu]['MCL'] /= runs

    return nmi_scores, time_scores

# Fixed parameter nmi_scores['mu']['Louvain'] and nmi_scores['mu']['Fluid Communities']
# If we add other algorithms, we can do so in this way
def plot_nmi_scores(nmi_scores, time_scores):
    mu_values = list(nmi_scores.keys())
    nmi_louvain = np.array([nmi_scores[mu]['Louvain'] for mu in mu_values])
    nmi_fluidc = np.array([nmi_scores[mu]['Fluid Communities'] for mu in mu_values])
    nmi_mcl = np.array([nmi_scores[mu]['MCL'] for mu in mu_values])
    louvain_times = [time_scores[mu]['Louvain'] for mu in mu_values]
    fluidc_times = [time_scores[mu]['Fluid Communities'] for mu in mu_values]
    mcl_times = [time_scores[mu]['MCL'] for mu in mu_values]
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(mu_values, nmi_louvain, label='Louvain')
    plt.scatter(mu_values, nmi_louvain, marker='^')
    plt.xlabel('Mu')
    plt.ylabel('NMI')
    plt.title('Louvain')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(mu_values, nmi_fluidc, label='Fluid Communities')
    plt.scatter(mu_values, nmi_fluidc, marker='^')
    plt.xlabel('Mu')
    plt.ylabel('NMI')
    plt.title('Fluid Communities')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(mu_values, nmi_mcl, label='MCL')
    plt.scatter(mu_values, nmi_mcl, marker='^')
    plt.xlabel('Mu')
    plt.ylabel('NMI')
    plt.title('MCL')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(mu_values, louvain_times, label='Louvain')
    plt.plot(mu_values, fluidc_times, label='Fluid Communities')
    plt.plot(mu_values, mcl_times, label='MCL')
    plt.xlabel('Mu')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Completion Time')
    plt.legend()

    # Plot the difference in NMI scores

    plt.tight_layout()
    plt.show()

def plot(graph):
    plot_graph(graph)

def run(mu_values, N, k, average_degree, min_communities):
    nmi_scores, time_scores = calculate_average_nmi_for_mu_values(mu_values, N, k, average_degree, min_communities)
    print(nmi_scores)
    print(time_scores)
    plot_nmi_scores(nmi_scores, time_scores)
