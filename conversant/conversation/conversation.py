from typing import NamedTuple, Callable, Sequence, Iterable, Tuple, List, Any

from anytree import NodeMixin


class NodeData(NamedTuple, NodeMixin):
    """
    the data each node in the conversation holds.
    """
    node_id: str = ""
    author: str = ""
    timestamp: int = 0
    data: dict = dict()


class ConversationNode(NodeMixin):

    def __init__(self, parent: 'ConversationNode' = None, children: List['ConversationNode'] = None, node_data: NodeData = None, **kwargs):
        self.parent = parent
        self.children = children or []
        self.node_data = node_data or NodeData()
        self.node_data.data.update(kwargs)

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

    def prune(self, condition: Callable[[NodeData], bool]) -> 'Conversation':
        """
        prune the tree at the nodes that satisfying the condition, inclusively
        Args:
            condition: a function that receive a 'NodeData' as an argument and returns a boolean, used to choose nodes to prune.

        Returns:
            A pruned conversation

        """
        pass

