from typing import List, Tuple, NamedTuple, Optional, Dict

import igraph


class ConversationNodeId(NamedTuple):
    index: int
    external_node_id: Optional[str]


class ConversationTreeVisNode(NamedTuple):
    node_id: ConversationNodeId
    author_id: str
    parent_id: ConversationNodeId
    timestamp: Optional[str]
    content: str


def build_tree(conversation_nodes: List[ConversationTreeVisNode]) -> Tuple[igraph.Graph, Dict[ConversationTreeVisNode, int]]:
    _, nodes = zip(*list(conv.iter_conversation()))
    nodes: List[ConversationNode]
    nodes_indices = {node.node_id: i for i, node in enumerate(nodes)}
    edges = [(nodes_indices[n.node_id], nodes_indices[n.parent_id]) for n in nodes if n.parent_id is not None]
    g = igraph.Graph(n=len(nodes), edges=edges)
    return g, nodes_indices