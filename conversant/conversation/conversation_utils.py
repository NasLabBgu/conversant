import heapq
from typing import Sequence, Iterable, Tuple, Callable, List

import pandas as pd

from conversant.conversation import Conversation, NodeData
from conversant.conversation.conversation import ConversationNode


def prune_authors(conversation: Conversation, authors: Sequence[str]):
    authors_set = set(authors)

    def filter_func(node_data: NodeData) -> bool:
        return node_data.author not in authors_set

    return conversation.prune(filter_func)


def iter_conversation_by_timestamp(root: ConversationNode, initial_depth: int = 0) -> Iterable[Tuple[int, NodeData]]:
    """
    walk the conversation tree by a custom order determined by node_comparator.
    Args:
        tree:
            the tree to iterate
        initial_depth:

    Returns:
        Generates pairs of tree nodes with their respective depth.
    """
    root_ts = root.timestamp
    nodes = [(root_ts, (initial_depth, root))]  # list of triplets of the form (timestamp, depth, node)
    while len(nodes) > 0:
        ts, (depth, next_node) = heapq.heappop(nodes)
        child_depth = depth + 1
        for c in next_node.get_children():
            heapq.heappush(nodes, (c.timestamp, (child_depth, c)))

        yield depth, next_node


def iter_conversation_branches(conversation: Conversation) -> Iterable[Tuple[NodeData, List[NodeData]]]:
    """
    walk the conversation tree and generate pairs of node and its corresponding branch leading to it.
    Args:
        conversation: A conversation to iterate over.

    Returns:
        Iterable of pairs of NodeData coupled with a list of all nodes in the branch preceding this node.
    """
    root = conversation.root
    current_branch_nodes: List[NodeData] = []     # Stores the previous nodes in the parsed branch
    for depth, node_data in root.iter_conversation_tree():
        # check if the entire current branch was parsed, and start walking to the next branch
        if depth < len(current_branch_nodes):
            del current_branch_nodes[depth:]    # pop all nodes until the common ancestor

        current_branch_nodes.append(node_data)
        yield node_data, current_branch_nodes[:]


def conversation_to_dataframe(conversation: ConversationNode) -> pd.DataFrame:
    """

    Args:
        conversation:

    Returns:

    """
    pass





