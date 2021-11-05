from typing import Iterable, Callable, Union, Dict, List, Any

import pandas as pd

from conversant.conversation import NodeData
from conversant.conversation.parse import ConversationParser


class DataFrameConversationReader(ConversationParser[pd.DataFrame, pd.Series]):
    """
    a class for parsing conversations from a DataFrame.
    """

    def __init__(self,
                 data_extraction_strategy: Union[Dict[str, Union[str, List[str]]], Callable[[pd.Series], NodeData]],
                 no_parent_value: Any = None,
                 conversation_id_column: str = None
                 ):
        """
        Args:
            data_extraction_strategy: (dict or callable)
                If dict is given, then it must contain at least 5 keys: 'node_id', 'author', 'timestamp', 'parent_id',
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
        self.conversation_id_column = conversation_id_column

    def extract_conversation_id(self, raw_conversation: pd.DataFrame) -> Any:
        if self.conversation_id_column is not None:
            return raw_conversation[self.conversation_id_column][0]

        return self.DEFAULT_CONVERSATION_ID

    def extract_node_data(self, raw_node: pd.Series) -> NodeData:
        node_data = self.extract_data(raw_node)
        if node_data.parent_id == self.no_parent_value:
            node_data = set_node_data_value(node_data, "parent_id", None)

        return node_data

    def iter_raw_nodes(self, raw_conversation: pd.DataFrame) -> Iterable[pd.Series]:
        for x in raw_conversation.iterrows():
            yield x[1]


def get_extract_data_func(
        data_extraction_strategy: Union[Dict[str, str], Callable[[pd.Series], NodeData]]
) -> Callable[[pd.Series], NodeData]:

    if isinstance(data_extraction_strategy, dict):
        return get_extract_data_func_from_dict(data_extraction_strategy)

    elif callable(data_extraction_strategy):
        return data_extraction_strategy

    raise ValueError(f"Not valid 'data_extraction_strategy' was given. Should be a dict or a callable, "
                     f"but argument of type {type(data_extraction_strategy)} was given")


def get_extract_data_func_from_dict(fields_mapping: Dict[str, str]) -> Callable[[pd.Series], NodeData]:
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

    def extract_data(row: pd.Series) -> NodeData:
        if other_data_fields is not None:
            data = {f: row.get(f) for f in other_data_fields}
        else:
            data = dict(row)

        return NodeData(
            row[node_id_field],
            row[author_field],
            row[timestamp_field],
            data,
            row.get(parent_id_field)
        )

    return extract_data


def set_node_data_value(node_data: NodeData, field: str, value: Any) -> NodeData:
    node_data = node_data._asdict()
    node_data[field] = value
    return NodeData(**node_data)
