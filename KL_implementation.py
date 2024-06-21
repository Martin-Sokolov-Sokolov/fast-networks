import networkx as nx

### Kernighan Lin Algorithm Implementation


########################################## NOT USED IN THE FINAL IMPLEMENTATION ##########################################


class KernighanLin():
    def __init__(self,graph : nx.Graph): 
        self.graph = graph ; 

    def create_partition(self,graph : nx.Graph,partitionsize =2): 
        nodelist  = graph.nodes() 
        graphsize = len(nodelist) 
        middle = graphsize // 2
        A_initial = nodelist[:middle]
        A_swapped = [False] * len(A_initial) #wether this element has been swapped or not. 
        B_initial = nodelist[middle:] 
        B_swapped = [False] * len(B_initial) 
        group_A_attributes = self.create_node_attribute_dict(A_initial,"partition",'A')
        group_B_attributes = self.create_node_attribute_dict(A_initial,"partition",'B')
        nx.set_node_attributes(graph,group_A_attributes)
        nx.set_node_attributes(graph,group_B_attributes) 
        self.set_D_values(graph)  
        group_A_swapable = set(A_initial)
        group_B_swapable = set(B_initial) 
        for _ in (graphsize)//2 : 
            max_gain = -1 * float("inf") # -infinity
            swaps = [] 
            for elem_a in group_A_swapable: 
                for elem_b in group_B_swapable: 
                    if self.isNeighbor(elem_a,elem_b): 
                        c_ab = 1
                    else: 
                        c_ab = 0 
                    gain = graph[elem_a]["D_value"] + graph[elem_b]["D_value"] - 2 * c_ab 
                    if gain >max_gain : 
                        best_pair = [elem_a,elem_b] 
                        max_gain  = gain 
            swaps.append((best_pair,max_gain)) # Add best swap to swaplist
            #swap A and B in partition 
            self.update_Node_partition(graph,[elem_a],'B')
            self.update_Node_partition(graph,[elem_b],'A')
            group_A_swapable.remove(elem_a)
            group_B_swapable.remove(elem_b) 






            



        return "implement list of sets for partition in size 2"
    def create_node_attribute_dictionary(self,nodelist,attribute_name,attribute):
        attrs = {} 
        for node in nodelist:
            attrs[node][{"{0}".format(attribute_name) : attribute}]
        return attrs
    
    
    def get_D_value(self,vertex_id): 
        D_value = 0 # D = Eexternal - Internal
        group_vertex = self.graph[vertex_id]["partition"]
        for neighbour in self.graph.neighbors(vertex_id): 
            if self.graph[neighbour]["partition"] == group_vertex: 
                D_value -= 1 
            else: 
                D_value += 1 
        return D_value
    
    def set_D_values(self, nodelist, graph: nx.Graph):
        for node in nodelist: 
            node_D_value = self.get_D_value(node)
            D_value_attribute = self.create_node_attribute_dictionary([node],"D_value",node_D_value)
            nx.set_node_attributes(graph, D_value_attribute)

    def isNeighbor(self, node_A, node_B,graph : nx.graph) -> bool:
        neighbors_a = graph.neighbors(node_A)
        if node_B in neighbors_a : 
            return True
        else: 
            return False
    def update_Node_partition(self,graph:nx.Graph,nodelist,new_partition):
        attrs = self.create_node_attribute_dictionary(nodelist,"partition",new_partition)
        nx.set_node_attributes(graph,attrs)
    

########################################## NOT USED IN THE FINAL IMPLEMENTATION ##########################################





