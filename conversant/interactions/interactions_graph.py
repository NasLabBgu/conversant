from collections import UserDict
from operator import itemgetter
from typing import Any, Dict, Callable, Set, Iterable

import networkx as nx


WEIGHT_FIELD_NAME = "weight"


class PairInteractionsData(UserDict):
    # TODO figure out immutability to this class - but only after the networkx graph has beeen initialied
    MAX_UPDATES = 2
    WEIGHT_FIELD = WEIGHT_FIELD_NAME

    def __init__(self, user1: Any, user2: Any, interactions: Dict[str, Any]):
        super(PairInteractionsData, self).__init__()
        self.data = dict(interactions)
        self.data.update({"user1": user1, "user2": user2})

    @property
    def user1(self) -> Any:
        return self["user1"]

    @property
    def user2(self) -> Any:
        return self["user2"]

    @property
    def interactions(self) -> Dict[str, Any]:
        return {interaction: value for interaction, value in self.data.items() if
                (interaction != "user1" and interaction != "user2")}

    @staticmethod
    def get_empty() -> 'PairInteractionsData':
        return PairInteractionsData(None, None, {})

    def set_weight(self, weight: float):
        self.data[self.WEIGHT_FIELD] = weight

    def calculate_weight(self, weight: Callable[['PairInteractionsData'], float]):
        self.data[self.WEIGHT_FIELD] = weight(self)

    def __repr__(self):
        return f"PairInteractionsData(user1={self.user1}, user2={self.user2}, interactions={self.interactions})"


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

    WEIGHT_FIELD = WEIGHT_FIELD_NAME

    def __init__(self, op: Any, interactions: Iterable[PairInteractionsData], directed: bool = False):
        self.directed = directed
        self.__graph = from_pair_interactions_data(interactions, directed)
        self.__op = op

    @property
    def graph(self) -> nx.Graph:
        return self.__graph

    @property
    def op(self) -> Any:
        return self.__op

    @property
    def interactions(self) -> Iterable[PairInteractionsData]:
        return map(itemgetter(2), self.graph.edges(data=True))

    def set_interaction_weights(self, weight: Callable[[PairInteractionsData], float]):
        for _, _, pair_data in self.__graph.edges(data=True):
            pair_data.calculate_weight(weight)

    def filter_interactions(self, condition: Condition, inplace: bool = False) -> 'InteractionsGraph':
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
            return InteractionsGraph(self.op, interactions_dict.values(), self.directed)

        # filter inplace
        filtered_edges = map(itemgetter(0, 1), filtered_pairs_data)
        self.__graph = self.__graph.edge_subgraph(filtered_edges)
        return self

    def get_subgraph(self, nodes: Set[Any], inplace: bool = False) -> 'InteractionsGraph':
        if inplace:
            self.__graph = self.__graph.subgraph(nodes)
            return self

        def is_pair_to_keep(pair: PairInteractionsData) -> bool:
            # if user1 is contained, then user2 is contained. otherwise the given interaction wouldn't exist.
            return pair.user1 in nodes

        return self.filter_interactions(condition=is_pair_to_keep, inplace=inplace)  # inplace is always False here.

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

        return self.get_subgraph(component_nodes, inplace=inplace)

    def get_op_connected_components(self, scc: bool = False, inplace: bool = False) -> 'InteractionsGraph':
        return self.get_author_connected_component(author=self.op, scc=scc, inplace=inplace)

    def get_core_interactions(self, inplace: bool = False) -> 'InteractionsGraph':
        """
        Reduce the graph to include only authors that interacted with at least two other different authors.
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

        def is_interaction_to_keep(pair: PairInteractionsData) -> bool:
            return (pair.user1 in core_nodes) and (pair.user2 in core_nodes)

        return self.filter_interactions(condition=is_interaction_to_keep, inplace=inplace)  # inplace always False here.


def from_pair_interactions_data(interactions: Iterable[PairInteractionsData], directed: bool = True) -> nx.Graph:
    """
    builds a graph where each interaction forms an edge, and the interaction data is preserved as the an edge data.
    Args:
        interactions: an iterable of `PairInteractionsData` elements
        directed: if True, the `InteractionGraph` will be directed, otherwise it won't.

    Returns:
        a new `InteractionGraph` object with the data contained in the given interactions.

    """
    interactions = filter(lambda p: p.user1 != p.user2, interactions)
    edgelist = ((pair_data.user1, pair_data.user2, pair_data) for pair_data in interactions)
    graph_type = InteractionsDataDiGraph if directed else InteractionsDataGraph
    graph = nx.from_edgelist(edgelist, graph_type)
    return graph


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
