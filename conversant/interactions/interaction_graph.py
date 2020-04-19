import networkx as nx
import anytree
import pandas as pd


class InteractionGraph(object):
    def __init__(self, interactions_graph: nx.Graph):
        validate_interaction_graph(interactions_graph)
        self.interactions_graph = interactions_graph

    def get_core_interactions(self) -> nx.Graph:
        pass

    @staticmethod
    def from_anytree(conversation: anytree.Node) -> 'InteractionGraph':
        return interactions_graph_from_anytree_conversation(conversation)

    @staticmethod
    def from_dataframe(conversation: pd.DataFrame) -> 'InteractionGraph':
        return interactions_graph_from_dataframe_conversation(conversation)


def validate_interaction_graph(interactions_graph: nx.Graph) -> None:
    """ יו
    validate that the interaction graph was properly built.
    Args:
        interactions_graph:

    Returns:

    """
    if isinstance(interactions_graph, (nx.DiGraph, nx.MultiGraph)):
        raise TypeError(f"interactions graph of type {type(interactions_graph)} is not supported."
                        f"\nOnly undirected (not multi) graphs are currently supported")


def interactions_graph_from_anytree_conversation(conversation: anytree.Node) -> InteractionGraph:
    pass

def interactions_graph_from_dataframe_conversation(conversation: pd.DataFrame) -> InteractionGraph:
    pass




