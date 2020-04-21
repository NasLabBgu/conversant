from typing import Any, Dict

from conversant.conversation import Conversation
from conversant.conversation.conversation_utils import iter_conversation_branches
from conversant.interactions import InteractionsGraph, InteractionsAggregator


class InteractionsParser(object):
    def __init__(self, directed: bool = True, *aggregators: InteractionsAggregator):
        self.directed = directed
        self.__aggregators: Dict[str, InteractionsAggregator] = {agg.name: agg for agg in aggregators}

    def parse(self, conversation: Conversation) -> InteractionsGraph:
        # collect interaction values
        interactions = {}
        for node, branch in iter_conversation_branches(conversation):
            for interaction_name, aggregator in self.__aggregators.items():
                for u1, u2, interaction in aggregator.extract(node, branch, conversation):
                    users_key = self.__get_users_pair_key(u1, u2)
                    if users_key not in interactions:
                        interactions[users_key] = self.__initialize_interactions_containers()

                    aggregator.add(u1, u2, interaction, interactions[users_key][interaction_name])

        # aggregate values and finalize result
        collected_interactions = interactions
        interactions = {}
        for pair_key, pair_data in collected_interactions.items():
            pair_interactions = {}
            for interaction_type, aggregator in self.__aggregators.items():
                pair_interactions[interaction_type] = aggregator.aggregate(pair_data[interaction_type])

            interactions[pair_key] = pair_interactions

        return InteractionsGraph(interactions, self.directed)

    def __get_users_pair_key(self, u1: Any, u2: Any) -> tuple:
        if not self.directed:
            if u1 > u2:
                u1, u2 = u2, u1

        return u1, u2

    def __initialize_interactions_containers(self):
        return {name: agg.initialize_interactions_container() for name, agg in self.__aggregators.items()}



