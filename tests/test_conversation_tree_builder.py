from typing import Tuple, Iterable, Any
from unittest import TestCase

from conversant.conversation import NodeData
from conversant.conversation.conversation_tree_builder import build_conversation_from_ordered


class ConversationBuilderTest(TestCase):
    def test_build_conversation_tree(self):
        self.fail()

    def test_sort_nodes_from_children_map(self):
        self.fail()

    def test_build_conversation_from_ordered(self):
        nodes = generate_ordered_nodes_data()

        # sanity
        conversation = build_conversation_from_ordered(nodes)
        conversation



def generate_ordered_nodes_data() -> Iterable[Tuple[NodeData, Any, Any]]:
    nodes = [
        (NodeData(), 0, None),  # root
        (NodeData(), 1, 0),
        (NodeData(), 2, 0),
        (NodeData(), 3, 2),
        (NodeData(), 4, 1),
        (NodeData(), 5, 1),
        (NodeData(), 6, 2),
        (NodeData(), 7, 5),
    ]
    yield from nodes


