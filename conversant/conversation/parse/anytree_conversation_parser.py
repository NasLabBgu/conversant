from typing import Iterable, Callable, Union

from anytree import NodeMixin, AnyNode, Node, PreOrderIter

from conversant.conversation import NodeData
from conversant.conversation.parse import ConversationParser

NodeType = Union[NodeMixin, AnyNode, Node]


class AnyTreeConversationParser(ConversationParser[NodeType, NodeType]):

    def __init__(self, extract_data: Callable[[NodeType], NodeData]):
        super(AnyTreeConversationParser, self).__init__()
        self.extract_data = extract_data

    def extract_node_data(self, raw_node: NodeType) -> NodeData:
        return self.extract_data(raw_node)

    def iter_raw_nodes(self, raw_conversation: NodeType) -> Iterable[NodeType]:
        for node in PreOrderIter(raw_conversation):
            yield node
