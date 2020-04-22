from typing import Any, Tuple, Dict, NamedTuple

import networkx as nx


class PairInteractionsData(dict):
    def __init__(self, user1: Any, user2: Any, interactions: Dict[str, Any]):
        super().__init__()
        self.update({"user1": user1, "user2": user2})
        self.update(interactions)

        self.interaction_names = list(interactions.keys())

    @property
    def user1(self) -> Any:
        return self["user1"]

    @property
    def user2(self) -> Any:
        return self["user2"]

    @property
    def interactions(self) -> Dict[str, Any]:
        return {interaction: value for interaction, value in self.items() if (interaction != "user1" and interaction!= "user2")}

    @staticmethod
    def get_empty() -> 'PairInteractionsData':
        return PairInteractionsData(None, None, {})

    def __repr__(self):
        return f"PairInteractionsData(user1={self.user1}, user2={self.user2}, interactions={self.interactions})"

    # def __setitem__(self, key, value):
    #     raise TypeError("PairInteractionsData is immutable")
    #
    # def __delitem__(self, key):
    #     raise TypeError("PairInteractionsData is immutable")


class InteractionsDataGraph(nx.Graph):
    def initialize_pair_interactions_data(self) -> PairInteractionsData:
        return PairInteractionsData.get_empty()

    edge_attr_dict_factory = initialize_pair_interactions_data


class InteractionsDataDiGraph(nx.DiGraph):
    def initialize_pair_interactions_data(self) -> PairInteractionsData:
        return PairInteractionsData.get_empty()

    edge_attr_dict_factory = initialize_pair_interactions_data


InteractionsDict = Dict[Tuple[Any, Any], PairInteractionsData]


class InteractionsGraph(object):
    def __init__(self, interactions_dict: InteractionsDict, directed: bool = False):
        self.directed = directed
        self.__graph = interactions_dict_to_graph(interactions_dict, directed)


    @property
    def graph(self) -> nx.Graph:
        return self.__graph

    @property
    def interactions_dict(self) -> InteractionsDict:
        return {(u1, u2): data for u1, u2, data in self.graph.edges(data=True)}

    def get_core_interactions(self) -> 'InteractionsGraph':
        pass


def interactions_dict_to_graph(interactions_dict: InteractionsDict, directed: bool = True) -> nx.Graph:
    edgelist = ((pair_data.user1, pair_data.user2, pair_data) for pair_data in interactions_dict.values())
    graph_type = InteractionsDataDiGraph if directed else InteractionsDataGraph
    return nx.from_edgelist(edgelist, graph_type)

