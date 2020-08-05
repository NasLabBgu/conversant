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

    def iter_conversation_tree(self, init_depth: int = 0, max_depth: int = None) -> Iterable[Tuple[int, NodeData]]:
        """
        walk in DFS style on the given tree from left to right, and generates pairs of the current depth in the tree with the current node.
        Args:
            init_depth: The depth of the given tree root (it might be a subtree for example).
            max_depth: Limit the depth of the node to yield.

        Returns:
            Generates pairs of tree nodes with their respective depth.
        """
        if (max_depth is None) or (init_depth < max_depth):
            yield init_depth, self.node_data

            if (max_depth is None) or (init_depth + 1 < max_depth):
                for subtree in self.children:
                    yield from subtree.iter_conversation_tree(init_depth=init_depth + 1, max_depth=max_depth)


class Conversation(object):
    """
    A conversation object that handles a conversation tree
    """

    def __init__(self, conversation_tree: ConversationNode):
        self.__tree = conversation_tree

    @property
    def root(self) -> ConversationNode:
        return self.__tree

    @property
    def participants(self) -> Iterable[Any]:
        """
        a collection of all the authors who participate in this conversation.
        Returns:
            an
        """
        unique_authors = set(node_data.author for _, node_data in self.iter_conversation())
        return unique_authors

    def iter_conversation(self, init_depth: int = 0, max_depth: int = None
                          ) -> Iterable[Tuple[int, NodeData]]:
        """
        walk in DFS style on the given conversation from left to right, and generates pairs of the current depth in the tree with the current node.
        Args:
            conversation: the conversation to iterate over
            init_depth: The depth of the given tree root (it might be a subtree for example).
            max_depth: Limit the depth of the node to yield.

        Returns:
            Generates pairs of tree nodes with their respective depth.
        """
        return self.root.iter_conversation_tree(init_depth, max_depth)


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

