from lfr_benchmark import create_graph

def main():

    # Example of how to use the create_graph function
    # Tough to hit what parameters to use in order for this to work
    # Fortunately there is good documentation for the LFR_benchmark_graph function
    # https://networkx.org/documentation/stable/reference/generated/networkx.generators.community.LFR_benchmark_graph.html
    graph = create_graph(N = 250, k = 3, mu = 0.1, average_degree = 5, min_communities = 20)
    print(graph)

if __name__ == "__main__":
    main()