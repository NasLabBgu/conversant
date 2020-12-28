from typing import Iterable, Callable, Union, Dict, List, Any, NamedTuple

from conversant.conversation import NodeData
from conversant.conversation.parse import ConversationParser


class NamedTupleConversationReader(ConversationParser[Iterable[NamedTuple], NamedTuple]):
    """
    a class for parsing conversations from a iterable of NamedTuples.
    """
    def __init__(self,
                 data_extraction_strategy: Union[Dict[str, Union[str, List[str]]], Callable[[NamedTuple], NodeData]],
                 no_parent_value: Any = None
                 ):
        """
        Args:
            data_extraction_strategy: (dict or callable)
                If dict is given, then it must contain at least 4 keys: 'node_id', 'author', 'timestamp', 'parent_id',
                where each of these is mapped to the corresponding field name in the DataFrames to be parsed. additional
                key might be 'data' and should be mapped to a sequence of field names to take as data for each node
                in the conversation. if 'data' is not given, all additional fields are taken as data for each node.
                If callable is given, then it is used directly to extract data from each row in the DataFrame
                to form a new NodeData object.

            no_parent_value: (any type)
                a node with this value as a parent_id, is considered as it has no parent.
        """
        super().__init__()
        self.extract_data = get_extract_data_func(data_extraction_strategy)
        self.no_parent_value = no_parent_value

    def extract_node_data(self, raw_node: NamedTuple) -> NodeData:
        node_data = self.extract_data(raw_node)
        if node_data.parent_id == self.no_parent_value:
            node_data = set_node_data_value(node_data, "parent_id", None)

        return node_data

    def iter_raw_nodes(self, raw_conversation: Iterable[NamedTuple]) -> Iterable[NamedTuple]:
        yield from raw_conversation


def get_extract_data_func(
        data_extraction_strategy: Union[Dict[str, str], Callable[[NamedTuple], NodeData]]
) -> Callable[[NamedTuple], NodeData]:

    if isinstance(data_extraction_strategy, dict):
        return get_extract_data_func_from_dict(data_extraction_strategy)

    elif callable(data_extraction_strategy):
        return data_extraction_strategy

    raise ValueError(f"Not valid 'data_extraction_strategy' was given. Should be a dict or a callable, "
                     f"but argument of type {type(data_extraction_strategy)} was given")


def get_extract_data_func_from_dict(fields_mapping: Dict[str, str]) -> Callable[[NamedTuple], NodeData]:
    """

    Args:
        fields_mapping: (dict)
                must contain at least 4 keys: 'node_id', 'author', 'timestamp', 'parent_id',
                where each of these is mapped to the corresponding field name in the DataFrames to be parsed. additional
                key might be 'data' and should be mapped to a sequence of field names to take as data for each node
                in the conversation. if 'data' is not given, all additional fields are taken as data for each node.:

    Returns: a callable that extract data from a row in the DataFrame to form a NodeData object.
    """
    node_id_field = fields_mapping["node_id"]
    author_field = fields_mapping["author"]
    parent_id_field = fields_mapping["parent_id"]
    timestamp_field = fields_mapping["timestamp"]
    other_data_fields: List[str] = fields_mapping.get("data")  # if exists, should be a list of fields (str values)

    def extract_data(raw_node: NamedTuple) -> NodeData:
        node = raw_node._asdict()
        if other_data_fields is not None:
            data = {f: node.get(f) for f in other_data_fields}
        else:
            data = dict(node)

        return NodeData(
            node[node_id_field],
            node[author_field],
            node[timestamp_field],
            data,
            node.get(parent_id_field)
        )

    return extract_data


def set_node_data_value(node_data: NodeData, field: str, value: Any) -> NodeData:
    node_data = node_data._asdict()
    node_data[field] = value
    return NodeData(**node_data)
