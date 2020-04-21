import networkx as nx


class InteractionsGraph(object):
    def __init__(self, interactions_dict: dict, directed: bool = False):
        self.interactions_dict = interactions_dict
        self.directed = directed
        self.__graph = interactions_dict_to_graph(interactions_dict, directed)

    def get_core_interactions(self) -> nx.Graph:
        pass


def interactions_dict_to_graph(interactions_dict: dict, directed: bool = True) -> nx.Graph:
    edgelist = ((pair[0], pair[1], interactions_data) for pair, interactions_data in interactions_dict.items())
    grap_type = nx.DiGraph if directed else nx.Graph
    return nx.from_edgelist(edgelist, grap_type)





