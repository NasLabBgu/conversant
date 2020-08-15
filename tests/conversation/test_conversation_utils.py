from typing import List, Tuple
from unittest import TestCase

from anytree import LevelOrderGroupIter

from conversant.conversation import NodeData, ConversationNode, Conversation
from conversation.conversation_utils import iter_conversation_branches, iter_conversation_by_timestamp, \
    conversation_to_dataframe


class ConversationUtilsTest(TestCase):

    def test_iter_conversation(self):
        conversation, nodes_by_dfs_order = generate_conversation_with_ordered_nodes()
        iteration = list(conversation.iter_conversation())
        self.iter_conversation_tree_test_util(conversation.root, nodes_by_dfs_order, iteration)

    def test_iter_conversation_tree(self):
        conversation, nodes_by_dfs_order = generate_conversation_with_ordered_nodes()
        iteration = list(conversation.root.iter_conversation_tree())
        self.iter_conversation_tree_test_util(conversation.root, nodes_by_dfs_order, iteration)

    def iter_conversation_tree_test_util(self,
                                         tree: ConversationNode,
                                         nodes_by_dfs_order: List[ConversationNode],
                                         iteration_result: List[Tuple[int, NodeData]]
                                         ):
        depths, nodes = zip(*iteration_result)
        for expected_node, actual_node in zip(nodes_by_dfs_order, nodes):
            self.assertEqual(expected_node, actual_node)

        depth_groups = [[node for node in children] for children in LevelOrderGroupIter(tree)]
        depth_mapping = {node_data: i for i in range(len(depth_groups)) for node_data in depth_groups[i]}
        for node, actual_depth in zip(nodes_by_dfs_order, depths):
            expected_depth = depth_mapping[node]
            self.assertEqual(expected_depth, actual_depth)

    def test_walk_branches(self):
        conversation, nodes_by_dfs_order = generate_conversation_with_ordered_nodes()
        expected_depths, expected_nodes = zip(*list(conversation.iter_conversation()))

        iteration = list(iter_conversation_branches(conversation))
        actual_nodes, branches = zip(*iteration)
        actual_depth = [len(branch) - 1 for branch in branches]

        # sanity
        self.assertListEqual(list(expected_nodes), list(actual_nodes))
        self.assertListEqual(list(expected_depths), actual_depth)

        # deeper test
        root = conversation.root
        for node, branch in iteration:
            current_node = node
            reversed_branch = list(reversed(branch))
            for i in range(len(branch)):
                if i == len(branch) - 1:
                    self.assertEqual(root, reversed_branch[i])
                else:
                    self.assertEqual(current_node, reversed_branch[i])
                    self.assertEqual(current_node.parent_id, reversed_branch[i + 1].node_id)
                    current_node = reversed_branch[i + 1]

    def test_iter_conversation_by_timestamp(self):
        conversation, _ = generate_conversation_with_ordered_nodes()
        prev_timestamp = 0
        for depth, node in iter_conversation_by_timestamp(conversation.root):
            self.assertTrue(node.timestamp >= prev_timestamp)

    def test_conversation_to_dataframe(self):
        conversation, _ = generate_conversation_with_ordered_nodes()
        df = conversation_to_dataframe(conversation)
        print(df)


def generate_conversation_with_ordered_nodes() -> Tuple[Conversation, List[ConversationNode]]:
    """
    creates a toy conversation for testing
    Returns:
        a toy Conversation object
    """
    root = ConversationNode(NodeData(0, "op", parent_id=None, timestamp=0, data={"a": 0}))
    n1 = ConversationNode(NodeData(1, "u1", parent_id=0, timestamp=1, data={"a": 1}), parent=root)
    n2 = ConversationNode(NodeData(2, "u2", parent_id=0, data={"a": 2}), parent=root, timestamp=2)
    n3 = ConversationNode(NodeData(3, "op", parent_id=2, data={"a": 3}), parent=n2, timestamp=3, )
    n4 = ConversationNode(NodeData(4, "u3", parent_id=2, data={"a": 4}), parent=n2, timestamp=4)
    n5 = ConversationNode(NodeData(5, "op", parent_id=1, data={"a": 5}), parent=n1, timestamp=5)
    n6 = ConversationNode(NodeData(6, "u2", parent_id=3, data={"a": 6}), parent=n3, timestamp=6)
    n7 = ConversationNode(NodeData(7, "u1", parent_id=5, data={"a": 7}), parent=n5, timestamp=7)

    nodes_by_dfs_order = [root, n1, n5, n7, n2, n3, n6, n4]
    return Conversation(root), nodes_by_dfs_order

