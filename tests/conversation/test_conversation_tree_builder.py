from operator import itemgetter
from random import shuffle
from typing import Tuple, Iterable, Any, List, Dict
from unittest import TestCase

import networkx as nx
from matplotlib import pyplot

from conversant.conversation import NodeData
from conversant.conversation.conversation_builder import build_conversation_from_ordered, build_conversation, \
    sort_nodes_from_children_map
from interactions.reply_interactions_parser import get_reply_interactions_parser


class ConversationBuilderTest(TestCase):

    def test_build_conversation_tree(self):
        nodes, expected_dfs_order = list(generate_ordered_nodes_data())
        shuffle(nodes)

        # sanity
        conversation = build_conversation(nodes)
        _, actual_nodes = zip(*conversation.iter_conversation())
        actual_nodes_ids = list(map(itemgetter(0), actual_nodes))

        # check each node is visited only once, and all nodes are actually visited
        self.assertEqual(len(nodes), len(set(actual_nodes_ids)))

        # test correct order of branches
        # self.assertListEqual(expected_dfs_order, actual_nodes_ids)  # TODO find a way to check conversation correct order.

    def test_sort_nodes_from_children_map(self):
        children_map_input = generate_children_map()
        actual_sorted_nodes = sort_nodes_from_children_map(children_map_input)
        actual_sorted_ids = list(map(itemgetter(1), actual_sorted_nodes))

        children_ids_map = {parent_id: [child[1] for child in children]
                            for parent_id, children in children_map_input.items()}

        # test topological sort
        for parent in actual_sorted_ids[:-1]:
            for node in actual_sorted_ids[parent + 1:]:
                self.assertFalse(parent in children_ids_map.get(node, []))

    def test_build_conversation_from_ordered(self):
        nodes, expected_dfs_order = list(generate_ordered_nodes_data())

        # sanity
        conversation = build_conversation_from_ordered(nodes)
        _, actual_nodes = zip(*conversation.iter_conversation())
        actual_nodes_ids = list(map(itemgetter(0), actual_nodes))
        self.assertListEqual(expected_dfs_order, actual_nodes_ids)

        #edge cases
        no_root_nodes = nodes[1:]
        self.assertRaisesRegex(ValueError, "None parent", build_conversation_from_ordered, no_root_nodes)

    def test_interaction_graph(self):
        nodes, _ = list(generate_ordered_nodes_data())
        conversation = build_conversation_from_ordered(nodes)
        parser = get_reply_interactions_parser()
        ig = parser.parse(conversation)
        type(ig)
        isinstance(ig.graph, nx.Graph)

        layout = nx.spring_layout(ig.graph)
        nx.draw_networkx(ig.graph, layout)
        pyplot.show()




def generate_ordered_nodes_data() -> Tuple[Iterable[Tuple[NodeData, Any, Any]], List[int]]:
    nodes = [
        (NodeData(0, "op"), 0, None),  # root
        (NodeData(1, "u1"), 1, 0),
        (NodeData(2, "u2"), 2, 0),
        (NodeData(3, "op"), 3, 2),
        (NodeData(4, "u3"), 4, 2),
        (NodeData(5, "op"), 5, 1),
        (NodeData(6, "u2"), 6, 3),
        (NodeData(7, "u1"), 7, 5),
    ]
    nodes_id_by_dfs_order = [0, 1, 5, 7, 2, 3, 6, 4]
    return nodes, nodes_id_by_dfs_order


def generate_children_map() -> Dict[Any, List[Tuple[NodeData, Any, Any]]]:
    return {
        None: [(NodeData(0, "op"), 0, None)],
        0: [(NodeData(1, "u1"), 1, 0), (NodeData(2, "u2"), 2, 0)],
        1: [(NodeData(5, "op"), 5, 1)],
        2: [(NodeData(3, "op"), 3, 2), (NodeData(4, "u3"), 4, 2)],
        3: [(NodeData(6, "u2"), 6, 3)],
        5: [(NodeData(7, "u1"), 7, 5)]
    }







