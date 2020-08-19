from typing import Iterable, Tuple, Dict

import tqdm

from conversant.conversation import Conversation, ConversationNode, NodeData

import pandas as pd
import numpy as np
import networkx as nx


## Feature Extraction
from conversation.conversation_utils import iter_conversation_branches
from conversation.examples.reddit_conversation_reader import CMVConversationReader
from conversant.interactions.reply_interactions_parser import get_reply_interactions_parser


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

## interaction graph features

def get_clustering_coeff(graph :nx.graph) -> float:
    if len(graph) == 0:
        return 0

    return nx.average_clustering(graph)


def get_average_degree(graph: nx.graph) -> float:
    return float(np.mean([value for _, value in graph.degree()]))


def get_average_betweeness_centrality(graph: nx.graph) -> float:
    return float(np.mean([value for value in nx.betweenness_centrality(graph).values()]))


def get_two_core_size(graph: nx.Graph) -> int:
    return len(nx.k_core(graph,2))


def get_three_core_size(graph: nx.Graph) -> int:
    return len(nx.k_core(graph,3))


def get_two_core_to_full_graph_ratio(graph: nx.Graph) -> float:
    return len(nx.k_core(graph,2)) / len(graph)


def three_core_to_full_graph_ratio(graph: nx.Graph) -> float:
    return len(nx.k_core(graph,3)) / len(graph)


def get_features(conv: Conversation) -> Dict[str, float]:
    num_nodes = conv.size
    num_users = len(list(conv.participants))
    avg_out_degree = get_average_out_degree(conv)
    avg_out_degree_no_leaves = get_average_out_degree(conv, ignore_leaves=True)
    num_branches = len(list(iter_conversation_branches(conv)))
    average_users_per_branch = get_average_participants_per_branch(conv)
    avg_ts_diff, median_ts_diff = get_timestamp_diff_stats(conv)

    conversation_values = [
        conv.id, num_nodes, num_users, avg_out_degree, avg_out_degree_no_leaves,
        num_branches, average_users_per_branch, avg_ts_diff, median_ts_diff
    ]
    conversation_names = [
        "conv_id", "num_nodes", "num_users", "avg_out_degree", "avg_out_degree_no_leaves",
        "num_branches", "average_users_per_branch", "avg_ts_diff", "median_ts_dif"
    ]

    # exctract interactions graph features
    interactions_parser = get_reply_interactions_parser()
    interactions_graph = interactions_parser.parse(conv)
    g = interactions_graph.graph

    graph_size = len(g)
    cluster_coeff = get_clustering_coeff(g)
    avg_interactions_degree = get_average_degree(g)
    avg_betweeness = get_average_betweeness_centrality(g)
    two_core_size = get_two_core_size(g)
    three_core_size = get_three_core_size(g)
    two_core_ratio = float(two_core_size) / graph_size if graph_size > 0 else 0
    three_core_ratio = float(three_core_size) / graph_size if graph_size > 0 else 0

    interactions_values = [cluster_coeff, avg_interactions_degree, avg_betweeness, two_core_size, three_core_size, two_core_ratio, three_core_ratio]
    interactions_names = ["cluster_coeff", "avg_interactions_degree", "avg_betweeness", "two_core_size", "three_core_size", "two_core_ratio", "three_core_ratio"]

    # finalize
    values = conversation_values + interactions_values
    names = conversation_names + interactions_names
    return dict(zip(names, values))


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

