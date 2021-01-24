from collections import deque, Counter
from typing import Tuple, Any, Dict, Iterable, List

from conversant.conversation import NodeData, Conversation
from conversant.conversation.conversation import ConversationNode

EMPTY_SEQUENCE = tuple()
ROOT_PARENT = None


def build_conversation(nodes_data: Iterable[Tuple[NodeData, Any, Any]], conversation_id: Any = None, root_parent_value: Any = ROOT_PARENT) -> Conversation:
    """
    Takes an iterable of nodes paired with their parent id, and builds a conversation object from the nodes.
    the parent of the root should be None, and only a single root is supported.
    if multiple nodes will have a None parent, then result is undefined.
    Args:
        nodes_data:
            an iterable of tuples containing the node's data, node's id and its parent id,
            (i.e  a triplet of (node_data, 'node_id', 'parent_id') ).
        conversation_id:
            A unique identifier for the resulting conversation.
        root_parent_value:
            the id value of the root parent.

    Returns:
        a Conversation object
    """
    children_map = {}
    for node in nodes_data:
        parent_id = node[2]
        children = children_map.setdefault(parent_id, [])
        children.append(node)

    ordered_nodes = sort_nodes_from_children_map(children_map, root_parent_value)
    return build_conversation_from_ordered(ordered_nodes, conversation_id, root_parent_value)


def sort_nodes_from_children_map(children_map: Dict[Any, List[Tuple[NodeData, Any, Any]]],
                                 root_parent_value: Any = ROOT_PARENT
                                 ) -> Iterable[Tuple[NodeData, Any, Any]]:
    """
    generate the nodes in children_map ordered from parent to descendants,
    meaning that a node will be generated before its children, not necessarily adjacent to each other.
    Args:
        children_map:
            A mapping between a node id to a list of its children,
            where each children is a tuple of (child_data, child_id, parent_id).
        root_parent_value:
            This value is used in children_map as a key that mapped to the root of the conversation.

    Returns:
        A generator of triplets (tuple) containing node_data, node_id, parent_id
    """
    if root_parent_value not in children_map:
        root_parent_value = infer_root_parent(children_map)
    # perform topological sorting by performing bfs on 'children_map' starting from the root node.
    root_node = children_map[root_parent_value][0]  # get a children list with a single element which is the root.
    root_node = (root_node[0], root_node[1], None)
    nodes = deque([root_node])
    while len(nodes) > 0:
        next_node = nodes.pop()
        node_id = next_node[1]
        [nodes.appendleft(child) for child in children_map.get(node_id, EMPTY_SEQUENCE)] # TODO explain code
        yield next_node


def build_conversation_from_ordered(
        nodes_data: Iterable[Tuple[NodeData, Any, Any]],
        conversation_id: Any = None,
        root_parent_value: Any = ROOT_PARENT
) -> Conversation:
    """
    same functionality as 'build_conversation', but 'nodes_data' is assumed to be ordered such that
    a parent must occur as a node by itself before occurring as a parent.
    Args:
        nodes_data:
            an iterable of tuples containing the node's data, node's id and its parent id,
            (i.e  a triplet of (node_data, 'node_id', 'parent_id') ).
        conversation_id:
            A unique identifier of the returned conversation.
        root_parent_value:
            the id value of the parent of the root node. the default value is 'None'.

    Returns:
        a Conversation object.

    """
    nodes_data = iter(nodes_data)
    root_data, root_id, parent_id = next(nodes_data)
    # validate that the first element is the root.
    # if parent_id is not root_parent_value:
    #     raise ValueError(f"The first element in 'nodes_data' must be the root with a {ROOT_PARENT} parent,"
    #                      f"or equalt to a given 'root_parent_value',"
    #                      f"but given parent id was: {parent_id}")

    root_node = ConversationNode(node_data=root_data)
    nodes_map = {root_id: root_node}
    for data, node_id, parent_id in nodes_data:
        parent_node = nodes_map[parent_id] if parent_id != root_parent_value else None
        children_node = ConversationNode(parent=parent_node, node_data=data)
        nodes_map[node_id] = children_node

    return Conversation(root_node, conversation_id)


def infer_root_parent(children_map: Dict[Any, List[Tuple[NodeData, Any, Any]]]) -> Any:
    """
    find the parent id of a node that could be the used as the root of the conversation tree.
    If there are few such nodes, only one is selected in an undefined way.
    Args:
        children_map:

    Returns: the id of the parent of a possible root node.

    >>> d = {1: [(None, 2, 1), (None, 3, 1)], 2: [(None, 4, 2)]}
    >>> infer_root_parent(d)
    1

    >>> d[5] = [(None, 1, 5)]
    >>> infer_root_parent(d)
    5

    >>> d[None] = [(None, 5, None)]
    >>> print(infer_root_parent(d))
    None
    """
    parents_map = parent_map_from_children_map(children_map)
    possible_root_parents = [node_id for node_id in children_map if node_id not in parents_map]
    if len(possible_root_parents) == 0:
        raise RecursionError(
            "no possible root was found, the given children_map forms a cyclic graph rather than a tree")

    return possible_root_parents[0]


def parent_map_from_children_map(children_map: Dict[Any, List[Tuple[NodeData, Any, Any]]]) -> Dict[Any, Any]:
    """
    reverse the children_map into a parents map that maps node_id to its parent_id
    Args:
        children_map: a mpping between a node_id to its children (each child is a tuple of (data, node_id, child_id)

    Returns: a mapping between a node id to its parent id.

    """
    parents_map = {}
    for parent_id, children in children_map.items():
        for _, child_id, _ in children:
            parents_map[child_id] = parent_id

    return parents_map




