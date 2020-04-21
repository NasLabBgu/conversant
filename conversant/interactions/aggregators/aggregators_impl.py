from typing import List, Iterable, Tuple, Any, Callable

from conversant.conversation import NodeData, Conversation
from conversant.interactions.aggregators import InteractionsAggregator

ExtractFunc = Callable[[NodeData, List[NodeData], Conversation], Iterable[Tuple[Any, Any]]]


class CountInteractionsAggregator(InteractionsAggregator[None, int, list]):

    def __init__(self, interaction_name: str, extract_interaction: ExtractFunc):
        super().__init__(interaction_name)
        self.__extract_func = extract_interaction

    def initialize_interactions_container(self) -> list:
        return [0]

    def extract(self, node: NodeData, branch: List[NodeData], tree: Conversation) -> Iterable[Tuple[Any, Any, None]]:
        for u1, u2 in self.__extract_func(node, branch, tree):
            yield u1, u2, None

    def add(self, u1: Any, u2: Any, interaction_value: None, container: list):
        container[0] += 1

    def aggregate(self, container: list) -> int:
        return container[0]
