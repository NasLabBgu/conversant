from typing import NamedTuple, Callable, Sequence, Iterable, Tuple, List, Any, Union

from anytree import NodeMixin, RenderTree


class NodeData(NamedTuple):
    """
    the data each node in the conversation holds.
    """
    node_id: Any = ""
    author: str = ""
    timestamp: int = 0
    data: dict = dict()
    parent_id: Any = ""


class ConversationNode(NodeMixin):

    def __init__(self, node_data: NodeData = None, parent: 'ConversationNode' = None, children: List['ConversationNode'] = None, **kwargs):
        self.parent = parent
        self.__children = children
        self.__node_data = node_data or NodeData()
        self.node_data.data.update(kwargs)

        if children:
            self.children = children

    @property
    def node_data(self) -> NodeData:
        return self.__node_data

    @property
    def node_id(self) -> Any:
        return self.node_data.node_id

    @property
    def author(self) -> str:
        return self.node_data.author

    @property
    def timestamp(self) -> int:
        return self.node_data.timestamp

    @property
    def data(self) -> dict:
        return self.node_data.data


class Conversation(object):
    """
    A conversation object that handles a conversation tree
    """

    def __init__(self, conversation_tree: ConversationNode):
        self.__tree = conversation_tree

    @property
    def root(self) -> ConversationNode:
        return self.__tree

    def prune(self, condition: Callable[[NodeData], bool]) -> 'Conversation':
        """
        prune the tree at the nodes that satisfying the condition, inclusively
        Args:
            condition: a function that receive a 'NodeData' as an argument and returns a boolean, used to choose nodes to prune.

        Returns:
            A pruned conversation

        """
        pass

    def __repr__(self) -> str:
        return str(RenderTree(self.root).by_attr(lambda n: self.__repr_node(n)))

    def __repr_node(self, node: ConversationNode) -> str:
        return f"{node.author} - {node.node_id}"

