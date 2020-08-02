from collections import deque
from typing import Tuple, Any, Dict, Iterable, List

from conversant.conversation import NodeData, Conversation
from conversant.conversation.conversation import ConversationNode

EMPTY_SEQUENCE = tuple()


def build_conversation(nodes_data: Iterable[Tuple[NodeData, Any, Any]]) -> Conversation:
    """
    Takes an iterable of nodes paired with their parent id, and builds a conversation object from the nodes.
    the parent of the root should be None, and only a single root is supported.
    if multiple nodes will have a None parent, then result is undefined.
    Args:
        nodes_data: an iterable of tuples containing the node's data, node's id and its parent id,
        (i.e  a triplet of (node_data, 'node_id', 'parent_id') ).

    Returns:
        a Conversation object
    """
    children_map = {}
    for node in nodes_data:
        parent_id = node[2]
        children = children_map.setdefault(parent_id, [])
        children.append(node)

    ordered_nodes = sort_nodes_from_children_map(children_map)
    return build_conversation_from_ordered(ordered_nodes)


def sort_nodes_from_children_map(children_map: Dict[Any, List[Tuple[NodeData, Any, Any]]]) -> Iterable[Tuple[NodeData, Any, Any]]:
    """
    generate the nodes in children_map ordered from parent to descendants,
    meaning that a node will be generated before its children, not necessarily adjacent to each other.
    Args:
        children_map:
            A mapping between a node id to a list of its children,
            where each children is a tuple of (child_data, child_id, parent_id).

    Returns:
        A generator of triplets (tuple) containing node_data, node_id, parent_id
    """
    # perform topological sorting by performing bfs on 'children_map' starting from the root node.
    root_node = children_map[None]  # get a children list with a single element which is the root.
    nodes = deque(root_node)
    while len(nodes) > 0:
        next_node = nodes.pop()
        node_id = next_node[1]
        [nodes.appendleft(child) for child in children_map.get(node_id, EMPTY_SEQUENCE)] # TODO explain code
        yield next_node


def build_conversation_from_ordered(nodes_data: Iterable[Tuple[NodeData, Any, Any]]) -> Conversation:
    """
    same functionality as 'build_conversation', but 'nodes_data' is assumed to be ordered such that
    a parent must occur as a node by itself before occurring as a parent.
    Args:
        nodes_data: an iterable of tuples containing the node's data, node's id and its parent id,
        (i.e  a triplet of (node_data, 'node_id', 'parent_id') ).

    Returns:
        a Conversation object
    """
    nodes_data = iter(nodes_data)
    root_data, root_id, parent_id = next(nodes_data)
    # validate that the first element is the root.
    if parent_id is not None:
        raise ValueError(f"The first element in 'nodes_data' must be the root with a None parent,"
                         f"but given parent id was: {parent_id}")

    root_node = ConversationNode(node_data=root_data)
    nodes_map = {root_id: root_node}
    for data, node_id, parent_id in nodes_data:
        parent_node = nodes_map[parent_id] if parent_id is not None else None
        children_node = ConversationNode(parent=parent_node, node_data=data)
        nodes_map[node_id] = children_node

    return Conversation(root_node)



