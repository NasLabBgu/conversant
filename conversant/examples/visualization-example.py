""" intended to load sampled datasets for examples """

# load a conversation
# use visualization tree

from typing import Iterable, Dict, Any

import pandas as pd

from tqdm.auto import tqdm

from conversation import Conversation
from conversation.parse import DataFrameConversationReader

FIELDS_MAPPING = {
    "node_id": "post_id",
    "author": "author",
    "timestamp": "timestamp",
    "parent_id": "parent_post_id"
}

def load_conversations_from_dataframe(path: str) -> Iterable[Conversation]:
    df = pd.read_csv(path, low_memory=False)
    parser = DataFrameConversationReader(FIELDS_MAPPING, conversation_id_column="conversation_id")
    groups = df.groupby("conversation_id")
    for cid, raw_conversation in tqdm(groups, total=groups.ngroups):
        yield parser.parse(raw_conversation, conversation_id=cid)


def get_author_labels(conv: Conversation) -> Dict[Any, int]:
    labels = {}
    for depth, node in conv.iter_conversation():
        label = node.data["author_label"]
        if isinstance(label, str):
            print(node)
        if label >= 0:
            labels[node.author] = label

    return labels


def is_relevant_conversation(conv: Conversation) -> bool:
    return bool(get_author_labels(conv))