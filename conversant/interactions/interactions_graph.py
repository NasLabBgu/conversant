from operator import itemgetter
from typing import Any, Tuple, Dict, NamedTuple, Mapping, Callable

import networkx as nx


class PairInteractionsData(dict):
    MAX_UPDATES = 1

    def __init__(self, user1: Any, user2: Any, interactions: Dict[str, Any]):
        super().__init__()
        super().update({"user1": user1, "user2": user2}, )
        super().update(interactions, )

        self.__num_updates = 0

    @property
    def user1(self) -> Any:
        return self["user1"]

    @property
    def user2(self) -> Any:
        return self["user2"]

    @property
    def interactions(self) -> Dict[str, Any]:
        return {interaction: value for interaction, value in self.items() if
                (interaction != "user1" and interaction != "user2")}

    @staticmethod
    def get_empty() -> 'PairInteractionsData':
        return PairInteractionsData(None, None, {})

    def __repr__(self):
        return f"PairInteractionsData(user1={self.user1}, user2={self.user2}, interactions={self.interactions})"

    def update(self, __m: Mapping, **kwargs) -> None:
        if not isinstance(__m, PairInteractionsData):
            if self.__num_updates == self.MAX_UPDATES:
                raise TypeError("PairInteractionsData is updatable only with the same type")

        super().update(__m)
        self.__num_updates += 1

    def __setitem__(self, key, value):
        raise TypeError("PairInteractionsData is immutable")

    __delitem__ = __setitem__


class InteractionsDataGraph(nx.Graph):
    def initialize_pair_interactions_data(self) -> PairInteractionsData:
        return PairInteractionsData.get_empty()

    edge_attr_dict_factory = initialize_pair_interactions_data


class InteractionsDataDiGraph(nx.DiGraph):
    def initialize_pair_interactions_data(self) -> PairInteractionsData:
        return PairInteractionsData.get_empty()

    edge_attr_dict_factory = initialize_pair_interactions_data


# type aliases
InteractionsDict = Dict[Tuple[Any, Any], PairInteractionsData]
Condition = Callable[[PairInteractionsData], bool]


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

    def filter_users(self, condition: Condition, inplace: bool = False) -> 'InteractionsGraph':
        """
        filters author nodes out from the given interactions-graph.
        Args:
            condition: a function that receives a `NodeData` as an argument and returns a `bool`
                       to indicate if to retain an author node or to filter it out.
            inplace: indicate if to maintain the filtering in the given interaction graph, rather than creating a new object.

        Returns:
            returns an `InteractionsGraph` filtered from the authors that didn't satisfy the condition.
        """
        edges = self.graph.edges(data=True)
        filtered_pairs_data = [e for e in edges if condition(e[2])]
        interactions_dict = {e[:2]: e[2] for e in filtered_pairs_data}

        if not inplace:
            return InteractionsGraph(interactions_dict, self.directed)

        # filter inplace
        filtered_edges = map(itemgetter(0, 1), filtered_pairs_data)
        self.__graph = self.__graph.edge_subgraph(filtered_edges)
        return self

    def get_core_interactions(self) -> 'InteractionsGraph':
        pass


def interactions_dict_to_graph(interactions_dict: InteractionsDict, directed: bool = True) -> nx.Graph:
    edgelist = ((pair_data.user1, pair_data.user2, pair_data) for pair_data in interactions_dict.values())
    graph_type = InteractionsDataDiGraph if directed else InteractionsDataGraph
    return nx.from_edgelist(edgelist, graph_type)
