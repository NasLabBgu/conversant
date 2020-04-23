from operator import itemgetter
from typing import Any, Dict, Mapping, Callable, Set, Iterable

import networkx as nx


class PairInteractionsData(dict):
    MAX_UPDATES = 2

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
        # if not isinstance(__m, PairInteractionsData):
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
Condition = Callable[[PairInteractionsData], bool]


class InteractionsGraph(object):
    def __init__(self, interactions: Iterable[PairInteractionsData], directed: bool = False):
        self.directed = directed
        self.__graph = interactions_dict_to_graph(interactions, directed)

    @property
    def graph(self) -> nx.Graph:
        return self.__graph

    @property
    def interactions(self) -> Iterable[PairInteractionsData]:
        return map(itemgetter(2), self.graph.edges(data=True))

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

    def get_author_connected_component(self, author: Any, scc: bool = False,
                                       inplace: bool = False) -> 'InteractionsGraph':
        """
        Reduce the graph to include only the interactions that are related to the connected component of the author.
        Args:
            author: the author name as given were this interaction graph was built.
            scc: if True, finds the strongly connected component of the author, otherwise use weak connectivity.
                 if this Interaction-graph is not directed, this argument is ignored.
            inplace: indicates if to return a new object or to modify the current instance.

        Returns:
            an `InteractionGraph` reduced to the connected component of the author.
        """
        if self.directed:
            if scc:
                components = nx.strongly_connected_components(self.__graph)
            else:
                components = nx.weakly_connected_components(self.__graph)

            component_nodes = get_node_component(components, author)
        else:
            component_nodes = nx.node_connected_component(self.graph, author)

        if inplace:
            self.__graph = self.__graph.subgraph(component_nodes)
            return self

        def is_pair_to_keep(pair: PairInteractionsData) -> bool:
            # if user1 is contained, then user2 is contained. otherwise the given interaction wouldn't exist.
            return pair.user1 in component_nodes

        return self.filter_users(condition=is_pair_to_keep, inplace=inplace)  # inplace is always False here.

    def get_core_interactions(self, inplace: bool = False) -> 'InteractionsGraph':
        """
        Reduce the graph to include only authors that interacted with at least to other different authors.
        Args:
            inplace: if True modify this instance, otherwise create a new instance to return.

        Returns:
            returns a reduced `InteractionsGraph` that contains only the core interactions.
        """
        core_graph = nx.k_core(self.__graph, 2)

        if inplace:
            self.__graph = core_graph
            return self

        core_nodes = set(core_graph.nodes)

        def is_pair_to_keep(pair: PairInteractionsData) -> bool:
            return (pair.user1 in core_nodes) and (pair.user2 in core_nodes)

        return self.filter_users(condition=is_pair_to_keep, inplace=inplace)  # inplace is always False here.


def interactions_dict_to_graph(interactions: Iterable[PairInteractionsData], directed: bool = True) -> nx.Graph:
    """
    builds a graph where each interaction forms an edge, and the interaction data is preserved as the an edge data.
    Args:
        interactions: an iterable of `PairInteractionsData` elements
        directed: if True, the `InteractionGraph` will be directed, otherwise it won't.

    Returns:
        a new `InteractionGraph` object with the data contained in the given interactions.

    """
    edgelist = ((pair_data.user1, pair_data.user2, pair_data) for pair_data in interactions)
    graph_type = InteractionsDataDiGraph if directed else InteractionsDataGraph
    return nx.from_edgelist(edgelist, graph_type)


def get_node_component(components: Iterable[Set[Any]], node: Any) -> Set[Any]:
    """
    finds the component containing the given 'node'.
    Args:
        components: iterable of graph components (set of nodes). Each node should occur in a single component only.
        node: a node_id

    Returns:
        returns the component containing the node, and an empty set if the node wasn't found in any of the components.
    """
    for comp in components:
        if node in comp:
            return comp

    return set()
