import heapq
from typing import Sequence, Iterable, Tuple, Callable, List, Dict, Any, Union

import pandas as pd

from conversant.conversation import Conversation, NodeData
from conversant.conversation.conversation import ConversationNode


NODE_RECORD_BASE_FIELDS = ["node_id", "author", "parent_id", "depth", "is_root", "is_leaf", "timestamp"]
# NODE_RECORD_BASE_FIELDS = ["node_id", "author", "parent_id", "depth", "timestamp"]


def prune_authors(conversation: Conversation, authors: Sequence[str]):
    authors_set = set(authors)

    def filter_func(node_data: NodeData) -> bool:
        return node_data.author not in authors_set

    return conversation.prune(filter_func)


def iter_conversation_by_timestamp(root: ConversationNode, initial_depth: int = 0) -> Iterable[Tuple[int, ConversationNode]]:
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


def iter_conversation_branches(conversation: Conversation) -> Iterable[Tuple[ConversationNode, List[ConversationNode]]]:
    """
    walk the conversation tree and generate pairs of node and its corresponding branch leading to it.
    Args:
        conversation: A conversation to iterate over.

    Returns:
        Iterable of pairs of NodeData coupled with a list of all nodes in the branch preceding this node.
    """
    root = conversation.root
    current_branch_nodes: List[NodeData] = []     # Stores the previous nodes in the parsed branch
    for depth, node in root.iter_conversation_tree():
        # check if the entire current branch was parsed, and start walking to the next branch
        if depth < len(current_branch_nodes):
            del current_branch_nodes[depth:]    # pop all nodes until the common ancestor

        current_branch_nodes.append(node)
        yield node, current_branch_nodes[:]


def conversation_to_dataframe(conversation: Conversation, data_fields: List[str] = None) -> pd.DataFrame:
    """

    Args:
        conversation: the conversation to converat into a DataFrame
        data_fields: a list fields from the node's data to include in the DataFrame.
                The node's data is a dict and to include a deeper field
                the string should be the path to that field, separated by dots.

    Returns:


    """
    # path is also available if needed
    records = (
        {
            **get_base_data(node),
            **extract_node_data(node.data, data_fields)
         }
        for _, node in conversation.iter_conversation()
    )
    return pd.DataFrame.from_records(records, index="node_id")


def get_base_data(n: ConversationNode) -> Dict[str, Union[str, int, bool]]:
    NODE_RECORD_BASE_FIELDS = ["node_id", "author", "parent_id", "depth", "is_root", "is_leaf", "timestamp"]
    parent_id = None if n.parent is None else n.parent.node_id
    base_values = [n.node_id, n.author, parent_id, n.depth, n.is_root, n.is_leaf, n.timestamp]
    return dict(zip(NODE_RECORD_BASE_FIELDS, base_values))


def extract_node_data(data: dict, fields: List[str] = None) -> Dict[str, Any]:
    flat_data = flatten_dict(data) if fields is None \
        else extract_data_from_fields(data, fields)

    return {f"data.{k}": v for k, v in flat_data.items()}


def extract_data_from_fields(data: dict, fields: List[str]) -> Dict[str, Any]:
    """
    extract the data according to the given fields. each field might be recursive, separated by dots
    Args:
        data:
        fields:

    Returns: a new dictionary with the given fields and the corresponding values.

    >>> d = {"a": 1, "b": 2, "c": {"x": 7, "y": 9}}
    >>> extract_data_from_fields(d, ["a", "c.x"])
    {'a': 1, 'c.x': 7}
    """
    flat_data = {}
    for f in fields:
        path = f.split(".")
        value = data
        for p in path:
            value = value[p]

        flat_data[f] = value

    return flat_data


def flatten_dict(data: dict, prefix: str = None) -> Dict[str, Any]:
    """
    extract all data from a dict, recursively, and return it flattened - without inner dictionaries.
    recursive fields are marked with their path from the root separated by dots.
    Args:
        data: the dict to parse

    Returns: flattened dict
    >>> d = {"a": 1, "b": 1}
    >>> flatten_dict(d)
    {'a': 1, 'b': 1}

    >>> d["c"] = {"x": 3}
    >>> flatten_dict(d)
    {'a': 1, 'b': 1, 'c.x': 3}
    """
    if prefix is not None:
        prefix += "."
    else:
        prefix = ""

    flat_data = {}
    for k, v in data.items():
        field_name = f"{prefix}{k}"
        if isinstance(v, dict):
            subdata = flatten_dict(v, prefix=field_name)
            flat_data.update(subdata)
            continue

        flat_data[field_name] = v

    return flat_data


def extract_all_fields(data: dict) -> List[str]:
    """
    extract all fields from a dict, recursively.
    recursive fields are marked with their path from the root separated by dots.
    Args:
        data: the dict to parse

    Returns: list of fields in the dict

    >>> d = {"a": 1, "b": 1}
    >>> extract_all_fields(d)
    ['a', 'b']

    >>> d["c"] = {"x": 3}
    >>> extract_all_fields(d)
    ['a', 'b', 'c.x']
    """
    return list(flatten_dict(data).keys())

