# import abc
# from typing import IO, Any, TypeVar, Generic, Tuple, Iterable
#
# from conversant.conversation import NodeData
#
# T = TypeVar('T')
#
#
# class ConversationReader(Generic[T], abc.ABC):
#     """
#     An interface for a conversation reader instance that reads a conversation from a file.
#     this class should be implemented differently for different formats of conversations in files.
#     it may be any type of file (binary, buffered-binary or text).
#     """
#     @abc.abstractmethod
#     def extract_node_data(self, raw_node: T) -> NodeData:
#         """
#         Extracts data related to this node from the given 'raw' element. the
#         Args:
#             raw_node: A raw_node to be parsed to extract data.
#
#         Returns:
#             A NodeData instance with the data of the corresponding raw_node
#         """
#         raise NotImplementedError
#
#     @abc.abstractmethod
#     def iter_file(self, fd: IO) -> Iterable[T]:
#         raise NotImplementedError
#
#     def get_parent_id(self, node_data: NodeData) -> Any:
#         """
#         Extract a parent id from the node_data.
#         Args:
#             node_data: data extracted for a node.
#
#         Returns:
#             id of the parent of the node.
#         """
#         return node_data.parent_id
#
#     def get_node_id(self, node_data: NodeData) -> Any:
#         """
#         Extract the id of the node according to the node_data.
#         Args:
#             node_data: data extracted for a node.
#
#         Returns:
#             id of the corresponding node.
#         """
#         return node_data.node_id
#
#     def read(self, fd: IO) -> Iterable[Tuple[NodeData, Any, Any]]:
#         """
#         iterates a file-like object, extract data from each raw_element from the iteration.
#         Args:
#             fd: a file-like object
#
#         Returns:
#             iterable of triplets of (node_data, node_id, parent_id)
#         """
#         for raw_node in self.iter_file(fd):
#             node_data = self.extract_node_data(raw_node)
#             node_id = self.get_node_id(node_data)
#             parent_id = self.get_parent_id(node_data)
#             yield node_data, node_id, parent_id
#
#     def read_file(self, path: str, read_mode: str) -> Iterable[Tuple[NodeData, Any, Any]]:
#         """
#         Opens the file at the given path for reading, and iterates it to extract data from each raw_element from the iteration.
#         Args:
#             path: A path to a file to read
#             read_mode: the mode in which to read the file
#
#         Returns:
#             iterable of triplets of (node_data, node_id, parent_id)
#         """
#         with open(path, read_mode) as f:
#             return self.read(f)
#
