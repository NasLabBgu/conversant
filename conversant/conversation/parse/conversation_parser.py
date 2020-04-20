import abc
from typing import Any, TypeVar, Generic, Tuple, Iterable

from conversant.conversation import NodeData, Conversation
from conversant.conversation.conversation_builder import build_conversation

K = TypeVar('K')
T = TypeVar('T')


class ConversationParser(Generic[K, T], abc.ABC):
    """
    An interface for a conversation reader instance that reads a conversation from a file.
    this class should be implemented differently for different formats of conversations in files.
    it may be any type of file (binary, buffered-binary or text).
    """
    @abc.abstractmethod
    def extract_node_data(self, raw_node: T) -> NodeData:
        """
        Extracts data related to this node from the given 'raw' element. the
        Args:
            raw_node: A raw_node to be parsed to extract data.

        Returns:
            A NodeData instance with the data of the corresponding raw_node
        """
        raise NotImplementedError

    @abc.abstractmethod
    def iter_raw_nodes(self, raw_conversation: K) -> Iterable[T]:
        raise NotImplementedError

    def get_parent_id(self, node_data: NodeData) -> Any:
        """
        Extract a parent id from the node_data.
        Args:
            node_data: data extracted for a node.

        Returns:
            id of the parent of the node.
        """
        return node_data.parent_id

    def get_node_id(self, node_data: NodeData) -> Any:
        """
        Extract the id of the node according to the node_data.
        Args:
            node_data: data extracted for a node.

        Returns:
            id of the corresponding node.
        """
        return node_data.node_id

    def parse(self, raw_conversation: K) -> Conversation:
        conversation_components = self.__parse_to_triplets(raw_conversation)
        return build_conversation(conversation_components)

    def __parse_to_triplets(self, raw_conversation: K) -> Iterable[Tuple[NodeData, Any, Any]]:
        """
        iterates a file-like object, extract data from each raw_element from the iteration.
        Args:
            raw_conversation:

        Returns:
            iterable of triplets of (node_data, node_id, parent_id)
        """
        for raw_node in self.iter_raw_nodes(raw_conversation):
            node_data = self.extract_node_data(raw_node)
            node_id = self.get_node_id(node_data)
            parent_id = self.get_parent_id(node_data)
            yield node_data, node_id, parent_id
