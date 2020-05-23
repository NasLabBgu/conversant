from typing import Any, List, Iterable, Tuple

from conversant.conversation import NodeData, Conversation
from conversant.examples.cmv.cmv_interactions_utils import find_quote_author, check_delta_award, find_award_recipient
from conversant.examples.cmv.cmv_utils import find_user_mentions, strip_mention_prefix, find_quotes
from conversant.interactions import InteractionsParser
from conversant.interactions.aggregators import CountInteractionsAggregator
from examples.cmv.reddit_conversation_parser import CMVConversationReader

AUTHOR_FIELD = "author"
TEXT_FIELD = "text"
TIMESTAMP_FIELD = "timestamp"


def get_reply_interaction_users(node: NodeData, branch: List[NodeData], *args) -> Iterable[Tuple[Any, Any]]:
    if len(branch) < 2:
        return []

    parent_author = branch[-2].author
    return [(node.author, parent_author)]


def get_mentioned_users(node: NodeData, *args) -> Iterable[Tuple[Any, Any]]:
    text = node.data[TEXT_FIELD]
    mentions_positions = find_user_mentions(text)
    user_mentions = [strip_mention_prefix(text[slice(*mention_pos)]) for mention_pos in mentions_positions]
    author = node.author
    return ((author, mentioned) for mentioned in user_mentions)


def get_quoted_users(node: NodeData, branch: List[NodeData], tree: Conversation) -> Iterable[Tuple[Any, Any]]:
    text = node.data[TEXT_FIELD]
    timestamp = node.data[TIMESTAMP_FIELD]

    quotes_positions = find_quotes(text)
    quotes_authors = []
    for startpos, endpos in quotes_positions:
        quote = text[startpos: endpos]
        author = find_quote_author(quote, tree, reversed(branch), timestamp)
        if author is not None:
            quotes_authors.append(author)

    author = node.author
    return ((author, source_author) for source_author in quotes_authors)


def get_delta_users(node: NodeData, branch: List[NodeData], tree: Conversation) -> Iterable[Tuple[Any, Any]]:

    author = node.author
    text = node.data[TEXT_FIELD]
    op = tree.root.author

    delta_award_status = check_delta_award(author, text)
    if delta_award_status == 0:
        return []

    delta_recipient = find_award_recipient(text, delta_award_status)
    if delta_recipient == "OP":
        delta_recipient = op

    if delta_recipient is None:
        return []

    if delta_recipient != branch[-2].data[AUTHOR_FIELD]:
        if branch[-2].data[AUTHOR_FIELD] != "[deleted]":
            print(delta_recipient, branch[-2].data[AUTHOR_FIELD])
            delta_recipient = branch[-2].data[AUTHOR_FIELD]

    delta_giver = branch[-1].data[AUTHOR_FIELD]
    return [(delta_giver, delta_recipient)]


if __name__ == "__main__":
    conversation_file = "cmv-conversation-example.json"
    with open(conversation_file, 'r') as f:
        raw_conversation = f.read()

    cmv_reader = CMVConversationReader()
    conversation = cmv_reader.parse(raw_conversation)
    print(conversation)

    print()
    # participants
    unique_participants = conversation.participants
    for author in unique_participants:
        print(author)

    print()

    reply_counter = CountInteractionsAggregator("replies", get_reply_interaction_users)
    mention_counter = CountInteractionsAggregator("mentions", get_mentioned_users)
    quotes_counter = CountInteractionsAggregator("quotes", get_quoted_users)
    delta_counter = CountInteractionsAggregator("deltas", get_delta_users)

    interactions_parser = InteractionsParser(reply_counter, mention_counter, quotes_counter, delta_counter, directed=True)
    interaction_graph = interactions_parser.parse(conversation)
    [print(i) for i in interaction_graph.interactions]

    print(f"len(participants) == graph.order(): {len(unique_participants) == interaction_graph.graph.order()}")



