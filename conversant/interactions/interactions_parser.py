from conversant.conversation import Conversation
from conversant.interactions import InteractionsGraph, InteractionsAggregator


class InteractionsParser(object):
    def __init__(self, *aggregators: InteractionsAggregator):
        self.__aggregators = {agg.name: agg for agg in aggregators}

    def parse(self, conversation: Conversation) -> InteractionsGraph:
        interactions = {}
        root = conversation.root

