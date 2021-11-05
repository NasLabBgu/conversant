import abc
from typing import Any, TypeVar, Generic, Tuple, Iterable

from conversant.conversation import NodeData, Conversation
from conversant.conversation.conversation_builder import build_conversation

K = TypeVar('K')    # type of raw conversation
T = TypeVar('T')    # type of raw_node


class ConversationParser(Generic[K, T], abc.ABC):

    SPECIFIED_ROOT_PARENT_VALUE = "ROOT_PARENT"
    DEFAULT_CONVERSATION_ID = "ID_MISSING"
    """
    An interface for a conversation reader instance that reads a conversation from a file.
    this class should be implemented differently for different formats of conversations in files.
    it may be any type of file (binary, buffered-binary or text).
    Note: For any reader that inherits from this class, the id of the root node must not be None,
    as it is used as a special id symbol. Otherwise the behavior is undefined
    """
    @abc.abstractmethod
    def extract_conversation_id(self, raw_conversation: K) -> Any:
        """
        Extracts data related to this node from the given 'raw' element. the
        Args:
            raw_conversation: the conversation for which the id is returned

        Returns:
            A unique identifier for this conversation.
        """
        raise NotImplementedError

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

    def parse(self, raw_conversation: K, root_id: Any = None, conversation_id: Any = None) -> Conversation:
        """
        takes a raw conversation and build a `Conversation` instance from it.
        Args:
            raw_conversation: conversation tree to parse.
            root_id: force the node with this id to be the root of the conversation.
                     All ancestors and siblings of this node will be filtered out of the conversation.
            conversation_id: unique id of the given conversation

        Returns:
            a `Conversation` that represent the data in the given 'raw_conversation'.
        """
        conversation_components = self.__parse_to_triplets(raw_conversation, root_id)
        if conversation_id is None:
            try:
                conversation_id = self.extract_conversation_id(raw_conversation)
            except NotImplementedError:
                conversation_id = self.DEFAULT_CONVERSATION_ID

        root_parent_value = None if root_id is None else self.SPECIFIED_ROOT_PARENT_VALUE
        return build_conversation(conversation_components, conversation_id, root_parent_value)

    def __parse_to_triplets(self, raw_conversation: K, root_id: Any = None) -> Iterable[Tuple[NodeData, Any, Any]]:
        """
        iterates a file-like object, extract data from each raw_element from the iteration.
        Args:
            raw_conversation:
            root_id: force the node with this id to be the root of the conversation.
                     All ancestors and siblings of this node will be filtered out of the conversation.

        Returns:
            iterable of triplets of (node_data, node_id, parent_id)
        """
        root_found = False
        root_parent_value = None if root_id is None else self.SPECIFIED_ROOT_PARENT_VALUE
        for raw_node in self.iter_raw_nodes(raw_conversation):
            node_data = self.extract_node_data(raw_node)
            node_id = self.get_node_id(node_data)
            parent_id = self.get_parent_id(node_data)

            if (root_id is not None) and (node_id == root_id):
                parent_id = self.SPECIFIED_ROOT_PARENT_VALUE

            if parent_id is root_parent_value:
                if root_found:
                    raise ValueError("Multiple roots found (i.e nodes with None as a parent_id). Only a single root is allowed")

                root_found = True

            yield node_data, node_id, parent_id

        # if not root_found:
        #     raise ValueError(
        #         "No root found (i.e node with None as a parent_id)"
        #     )
