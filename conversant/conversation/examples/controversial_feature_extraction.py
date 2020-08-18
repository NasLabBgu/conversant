from typing import Iterable, Tuple, List, Dict

import tqdm

from conversation import Conversation, ConversationNode, NodeData

import pandas as pd
import numpy as np



## Feature Extraction
from conversation.conversation_utils import iter_conversation_with_branches, iter_conversation_branches
from conversation.examples.reddit_conversation_reader import CMVConversationReader


def get_average_out_degree(conv: Conversation, ignore_leaves: bool = False) -> float:
    num_nodes = conv.size
    num_children = [len(n.children) for _, n in conv.iter_conversation()]
    if ignore_leaves:
        num_nodes -= num_children.count(0)

    if num_nodes == 0:
        return 0

    return float(sum(num_children)) / num_nodes


def get_average_participants_per_branch(conv: Conversation) -> float:
    branches = list(iter_conversation_branches(conv))
    num_unique_users_per_branch = [len(set([node.author for node in branch])) for branch in branches]
    return sum(num_unique_users_per_branch) / len(branches)


def get_timestamp_diff_stats(conv: Conversation) -> Tuple[float, ...]:
    diffs = []
    for branch in iter_conversation_branches(conv):
        for i in range(1, len(branch)):
            diff = branch[i].timestamp - branch[i-1].timestamp
            diffs.append(diff)

    avg = float(np.mean(diffs))
    median = float(np.median(diffs))
    return avg, median


def get_features(conv: Conversation) -> Dict[str, float]:
    num_nodes = conv.size
    avg_out_degree = get_average_out_degree(conv)
    avg_out_degree_no_leaves = get_average_out_degree(conv, ignore_leaves=True)
    num_branches = len(list(iter_conversation_branches(conv)))
    average_users_per_branch = get_average_participants_per_branch(conv)
    avg_ts_diff, median_ts_diff = get_timestamp_diff_stats(conv)

    feature_names = ["num_nodes", "avg_out_degree", "avg_out_degree_no_leaves",
            "num_branches", "average_users_per_branch", "avg_ts_diff",
            "median_ts_dif"]
    features = [num_nodes, avg_out_degree, avg_out_degree_no_leaves, num_branches, average_users_per_branch, avg_ts_diff, median_ts_diff]
    return dict(zip(feature_names, features))


#### runner utils

def iter_trees_from_lines(data_path: str) -> Iterable[str]:
    with open(data_path, 'r') as f:
        yield from f


def generate_conversation() -> Conversation:
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
    return Conversation(root)


if __name__ == "__main__":
    ## cmv_example
    trees_file_path = r"C:\Users\ronp\Documents\stance-classification\trees_2.0.txt"
    total_trees = sum(1 for _ in iter_trees_from_lines(trees_file_path))
    trees = tqdm.tqdm(iter_trees_from_lines(trees_file_path), total=total_trees)
    conv_reader = CMVConversationReader()
    conversations = map(conv_reader.parse, trees)
    features = map(get_features, conversations)
    data = pd.DataFrame.from_records(features, index="conv_id")
    print(data.head())

