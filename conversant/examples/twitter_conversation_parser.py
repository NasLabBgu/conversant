from typing import Iterable

from conversant.conversation import NodeData
from conversant.conversation.parse import ConversationParser


class TwitterConversationParser(ConversationParser[str, str]):
    def extract_node_data(self, raw_node: str) -> NodeData:
        pass

    def iter_raw_nodes(self, raw_conversation: str) -> Iterable[str]:
        pass
