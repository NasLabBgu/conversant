from typing import List, Iterable, Tuple, Any

from conversant.conversation import Conversation
from conversant.interactions import InteractionsParser
from conversant.interactions.aggregators import CountInteractionsAggregator
from conversant.conversation import ConversationNode


def get_reply_interaction_users(node: ConversationNode, branch: List[ConversationNode], conversation: Conversation) -> Iterable[Tuple[Any, Any]]:
    """
    parse th reply interaction of the current node.
    This is to determine the parent's author
    and return the reply interaction as a pair of the current author to the parent's author.
    Args:
        node: the node for which the interaction is parsed
        branch: the branch from the root the current node. that last element in the branch is the current node itself.
        conversation: the whole conversation in which the current node resides.

    Returns: a list of size 1 that contains a pair (tuple) with the node's author as the first element
    and the parent's author as the second element.
    """
    if len(branch) < 2:
        return []

    parent_author = branch[-2].author
    return [(node.author, parent_author)]


def get_reply_interactions_parser(directed=False) -> InteractionsParser:
    """
    build an interactions parser that considers only reply interactions between users.
    Args:
        directed: if true, the returned parser object generates a directed graph
        where the direction of the reply is considered.

    Returns: an interactionsParser object that considers only replies.

    """
    reply_counter = CountInteractionsAggregator("replies", get_reply_interaction_users)
    return InteractionsParser(reply_counter, directed=directed)
