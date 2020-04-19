from typing import List, Tuple
from unittest import TestCase

from anytree import LevelOrderGroupIter

from conversant.conversation import Conversation
from conversant.conversation.conversation import ConversationNode, NodeData
from conversant.conversation.conversation_utils import iter_conversation_tree, iter_conversation


class ConversationUtilsTest(TestCase):

    def test_iter_conversation(self):
        conversation, nodes_by_dfs_order = generate_conversation_with_ordered_nodes()
        iteration = list(iter_conversation(conversation))
        self.iter_conversation_tree_test_util(conversation.root, nodes_by_dfs_order, iteration)

    def test_iter_conversation_tree(self):
        conversation, nodes_by_dfs_order = generate_conversation_with_ordered_nodes()
        iteration = list(iter_conversation_tree(conversation.root))
        self.iter_conversation_tree_test_util(conversation.root, nodes_by_dfs_order, iteration)

    def iter_conversation_tree_test_util(self,
                                         tree: ConversationNode,
                                         nodes_by_dfs_order: List[ConversationNode],
                                         iteration_result: List[Tuple[int, NodeData]]
                                         ):
        depths, nodes = zip(*iteration_result)
        for expected_node, actual_node in zip(nodes_by_dfs_order, nodes):
            self.assertEqual(expected_node.node_data, actual_node)

        depth_groups = [[node for node in children] for children in LevelOrderGroupIter(tree)]
        depth_mapping = {node_data: i for i in range(len(depth_groups)) for node_data in depth_groups[i]}
        for node, actual_depth in zip(nodes_by_dfs_order, depths):
            expected_depth = depth_mapping[node]
            self.assertEqual(expected_depth, actual_depth)


def generate_conversation_with_ordered_nodes() -> Tuple[Conversation, List[ConversationNode]]:
    """
    creates a toy conversation for testing
    Returns:
        a toy Conversation object
    """
    root = ConversationNode(NodeData(0, "op"))
    n1 = ConversationNode(NodeData(1, "u1"), parent=root)
    n2 = ConversationNode(NodeData(2, "u2"), parent=root)
    n3 = ConversationNode(NodeData(3, "op"), parent=n2)
    n4 = ConversationNode(NodeData(4, "u3"), parent=n2)
    n5 = ConversationNode(NodeData(5, "op"), parent=n1)
    n6 = ConversationNode(NodeData(1, "u2"), parent=n3)
    n7 = ConversationNode(NodeData(1, "u1"), parent=n5)

    # for pre, _, node in RenderTree(root):
    #     treestr = f"{pre}{node.node_data.node_id}"
    #     print(treestr.ljust(16), node.author)

    nodes_by_dfs_order = [root, n1, n5, n7, n2, n3, n6, n4]
    return Conversation(root), nodes_by_dfs_order

