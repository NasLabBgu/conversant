from typing import Iterable, List, Tuple, Any

import pandas as pd
from IPython.core.display import display

from conversation import NodeData
from conversation.parse import ConversationParser
from interactions.reply_interactions_parser import get_reply_interactions_parser


class Twitterconversationreader(ConversationParser[pd.DataFrame, pd.Series]):

    def __init__(self):
        super().__init__()


    def extract_node_data(self, raw_node: pd.Series) -> NodeData:
        node_id = raw_node.id_str
        author = raw_node.user_id_str
        timestamp = raw_node.created_at
        data = dict(raw_node)
        parent_id = data.get('in_reply_to_status_id_str')
        if parent_id == 'nan':
            parent_id = None
            print(node_id)

        return NodeData(node_id, author, timestamp, data, parent_id)

    def iter_raw_nodes(self, raw_conversation: pd.DataFrame) -> Iterable[pd.Series]:
        for x in raw_conversation.iterrows():
            yield x[1]


def get_reply_interaction_users(node: NodeData, branch: List[NodeData], *args) -> Iterable[Tuple[Any, Any]]:
    if len(branch) < 2:
        return []

    parent_author = branch[-2].author
    return [(node.author, parent_author)]


# class TwitterInteractionGraphBuilder(object):
#     def __init__(self):
#         reply_counter = CountInteractionsAggregator("replies", get_reply_interaction_users)
#
#         self.__interactions_parser = InteractionsParser(reply_counter, directed=False)
#
#     def build(self, conversation: Conversation) -> InteractionsGraph:
#         return self.__interactions_parser.parse(conversation)

reply_interactions_parser = get_reply_interactions_parser()


if __name__ == "__main__":
    sample = pd.read_json(
        r"C:\Users\ronp\PycharmProjects\twitter-scraper\convoscrape\response_exploration\conv-1203211859366576128\tweets.jsonl",
        lines=True,
        dtype={'in_reply_to_status_id_str': str, "id_str": str})

    cols = ['created_at', 'id_str', 'text', 'user_id_str', 'conversation_id_str', 'in_reply_to_status_id_str',
            'in_reply_to_screen_name']

    print(len(sample))
    sample = sample.filter(cols)
    sample = sample.loc[sample.conversation_id_str == 1203211859366576128]
    sample = sample.loc[sample.id_str != "1203416002626805760"]
    sample = sample.loc[sample.id_str != "1203416002626805765"]
    print(len(sample))

    twitter_reader = Twitterconversationreader()
    conversation = twitter_reader.parse(sample)
    print(f"number of participants: {len(list(conversation.participants))}")

    ig = reply_interactions_parser.parse(conversation)
    ig.get_core_interactions()
    print(ig)

    display(sample.loc[sample["id_str"] == "1203416002626805765"]["user_id_str"])
