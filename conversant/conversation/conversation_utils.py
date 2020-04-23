from typing import Sequence, Iterable, Tuple, Callable, List

import anytree
import pandas as pd

from conversant.conversation import Conversation, NodeData
from conversant.conversation.conversation import ConversationNode


def prune_authors(conversation: Conversation, authors: Sequence[str]):
    authors_set = set(authors)

    def filter_func(node_data: NodeData) -> bool:
        return node_data.author not in authors_set

    return conversation.prune(filter_func)


def iter_conversation(conversation: Conversation, init_depth: int = 0, max_depth: int = None
                      ) -> Iterable[Tuple[int, NodeData]]:
    """
    walk in DFS style on the given conversation from left to right, and generates pairs of the current depth in the tree with the current node.
    Args:
        conversation: the conversation to iterate over
        init_depth: The depth of the given tree root (it might be a subtree for example).
        max_depth: Limit the depth of the node to yield.

    Returns:

    """
    return iter_conversation_tree(conversation.root, init_depth, max_depth)


def iter_conversation_tree(tree: ConversationNode, init_depth: int = 0, max_depth: int = None
                           ) -> Iterable[Tuple[int, NodeData]]:
    """
    walk in DFS style on the given tree from left to right, and generates pairs of the current depth in the tree with the current node.
    Args:
        tree: the tree to iterate over
        init_depth: The depth of the given tree root (it might be a subtree for example).
        max_depth: Limit the depth of the node to yield.

    Returns:
        Generates pairs of tree nodes with their respective depth.
    """
    if (max_depth is None) or (init_depth < max_depth):
        yield init_depth, tree.node_data

        if (max_depth is None) or (init_depth + 1 < max_depth):
            for subtree in tree.children:
                yield from iter_conversation_tree(subtree, init_depth=init_depth + 1, max_depth=max_depth)


def iter_conversation_by_(tree: ConversationNode, comparator: Callable[[ConversationNode, ConversationNode], bool]
                          ) -> Iterable[Tuple[int, NodeData]]:
    """
    walk the conversation tree by a custom order determined by node_comparator.
    Args:
        tree:
            the tree to iterate
        comparator: a callable that makes comparisons between two 'ConversationNode's. returns a positive value if the
            first argument is smaller than the second, negative value if the opposite is true
            and 0 if they are equal.

    Returns:
        Generates pairs of tree nodes with their respective depth.
    """
    #TODO implement dijkstra style iteration - BFS with a priority queue that works with the given comparator
    pass


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
    for depth, node_data in iter_conversation_tree(root):
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





