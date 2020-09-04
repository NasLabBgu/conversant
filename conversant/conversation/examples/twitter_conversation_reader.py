from itertools import groupby
from operator import itemgetter
from typing import Iterable, List, Tuple, Any, Union, Sequence

import pandas as pd
from IPython.core.display import display

from conversation import NodeData, Conversation, ConversationNode
from conversation.conversation_utils import iter_conversation_by_timestamp
from conversation.parse import ConversationParser
from conversation.parse.dataframe_conversation_reader import DataFrameConversationReader
from interactions.reply_interactions_parser import get_reply_interactions_parser


class TwitterConversationReader(ConversationParser[pd.DataFrame, pd.Series]):
    """
    A class to parse a twitter conversation from a DataFrame as it was created from the twitter api.
    """

    DEFAULT_DATA = ['full_text', 'conversation_id_str', 'in_reply_to_screen_name']

    NODE_FIELDS_MAPPING = {
        "node_id": "id_str",
        "author": "user_id_str",
        "timestamp": "timestamp",
        "parent_id": "in_reply_to_status_id_str",
        "data": DEFAULT_DATA
    }

    ALL_DATA_FIELDS = "all"
    NO_DATA_FIELDS = "none"

    def __init__(self, extra_data_fields: Union[None, str, List[str]] = None):
        super().__init__()
        fields_mapping = {**self.NODE_FIELDS_MAPPING}
        if extra_data_fields == self.ALL_DATA_FIELDS:
            del fields_mapping["data"]
        elif extra_data_fields == self.NO_DATA_FIELDS:
            fields_mapping["data"] = []
        elif isinstance(extra_data_fields, Sequence):
            fields_mapping["data"] = extra_data_fields
        self.dataframe_parser = DataFrameConversationReader(fields_mapping, no_parent_value='nan')

    def extract_node_data(self, raw_node: pd.Series) -> NodeData:
        return self.dataframe_parser.extract_data(raw_node)

    def iter_raw_nodes(self, raw_conversation: pd.DataFrame) -> Iterable[pd.Series]:
        raw_conversation["timestamp"] = raw_conversation["created_at"].apply(pd.Timestamp.timestamp)
        for x in raw_conversation.iterrows():
            yield x[1]

    def parse(self, raw_conversation: pd.DataFrame, root_id: str = None) -> Conversation:
        conversation = super(TwitterConversationReader, self).parse(raw_conversation, root_id)
        return merge_sequential_tweets(conversation)

def merge_sequential_tweets(conversation: Conversation) -> Conversation:
    ordered_tweets = map(itemgetter(1), iter_conversation_by_timestamp(conversation.root))
    for author, tweets in groupby(ordered_tweets, key=lambda n: n.author):
        merge_tweets(tweets)

    return conversation

def merge_tweets(tweets: Iterable[ConversationNode]) -> ConversationNode:
    tweets = iter(tweets)
    first_tweet = next(tweets)
    main_data = first_tweet.data
    for field in list(main_data.keys()):
        main_data[field] = [main_data[field]]

    main_children = {n.node_id: n for n in first_tweet.get_children()}
    for i, tweet in enumerate(tweets):
        if tweet.node_id in main_children:
            del main_children[tweet.node_id]

        current_data = tweet.data
        for field in current_data:
            if field not in main_data:
                main_data[field] = [None for _ in range(i)]

            main_data[field].append(current_data[field])

        current_children = {n.node_id: n for n in tweet.get_children()}
        main_children.update(current_children)

        tweet.chldren = []
        tweet.parent = None
        del tweet

    first_tweet.children = list(main_children.values())
    return first_tweet







reply_interactions_parser = get_reply_interactions_parser()


if __name__ == "__main__":
    sample = pd.read_json(
        r"C:\Users\ronp\Documents\stance-classification\rumors_dataset\PHEME_veracity\full-conversations\499394221984714752\tweets.jsonl",
        lines=True,
        dtype={"in_reply_to_status_id_str": str, "id_str": str}
    )

    twitter_reader = TwitterConversationReader()
    conversation = twitter_reader.parse(sample, root_id="499394221984714752")
    print(conversation)
    print(f"number of participants: {len(list(conversation.participants))}")

    ig = reply_interactions_parser.parse(conversation)
    ig.get_core_interactions()
    print(ig)