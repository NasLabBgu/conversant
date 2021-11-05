from itertools import starmap
from typing import TypeVar, Iterable, Tuple, Any, Union, NamedTuple, Generic

from conversant.conversation.parse import ConversationParser
from conversation import Conversation

K = TypeVar('K')    # type of raw conversation
T = TypeVar('T')    # type of raw_node


class RawConversationInput(NamedTuple, Generic[K]):
    raw_conversation: K
    root_id: Any
    conversation_id: Any

    @staticmethod
    def get_instance(raw_conversation: K, root_id: Any = None, conversation_id: Any = None):
        return RawConversationInput(raw_conversation, root_id, conversation_id)


class MultipleConversationsParser:

    def __init__(self, parser: ConversationParser[K, T]):
        self.parser = parser

    def parse(self, raw_conversations: Iterable[RawConversationInput[K]]) -> Iterable[Conversation]:
        yield from starmap(self.parser.parse, raw_conversations)

    def parse_raw(self, raw_conversations: Iterable[K]) -> Iterable[Conversation]:
        yield from map(self.parser.parse, raw_conversations)
