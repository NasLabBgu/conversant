from operator import itemgetter
from typing import Callable

from conversant.conversation import NodeData
from conversant.interactions import InteractionsGraph

PairInteractionsData = dict

Condition = Callable[[PairInteractionsData], bool]


def filter_users(interactions: InteractionsGraph, condition: Condition, inplace: bool = False) -> InteractionsGraph:
    """
    filters author nodes out from the given interactions-graph.
    Args:
        interactions: the interactions graph to filter.
        condition: a function that receives a `NodeData` as an argument and returns a `bool`
                   to indicate if to retain an author node or to filter it out.
        inplace: indicate if to maintain the filtering in the given interaction graph, rather than creating a new object.

    Returns:
        returns an `InteractionsGraph` filtered from the authors that didn't satisfy the condition.
    """
    edges = interactions.graph.edges(data=True)
    filtered_pairs = [e for e in edges if condition(e[2])]



