from typing import Iterable, Any

import pandas as pd

from conversant.conversation import NodeData
from conversant.conversation.parse import ConversationParser


class DataFrameConversationReader(ConversationParser[pd.DataFrame, pd.Series]):

    def __init__(self, parent_field: str, no_parent_value: Any = None):
        super().__init__()
        self.parent_field = parent_field
        self.no_parent_value = no_parent_value

    def extract_node_data(self, raw_node: pd.Series) -> NodeData:
        node_id = raw_node.id_str
        author = raw_node.user_id_str
        timestamp = raw_node.created_at
        data = dict(raw_node)
        parent_id = data.get(self.parent_field)
        if parent_id == self.no_parent_value:
            parent_id = None

        return NodeData(node_id, author, timestamp, data, parent_id)

    def iter_raw_nodes(self, raw_conversation: pd.DataFrame) -> Iterable[pd.Series]:
        for x in raw_conversation.iterrows():
            yield x[1]