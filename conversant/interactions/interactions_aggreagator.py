import abc
from typing import TypeVar, List, Tuple, Any, Iterable, Container

from anytree import NodeMixin

N = TypeVar('N', bound=NodeMixin)
T = TypeVar('T')  # interaction value type
K = TypeVar('K')  # aggregated interactions value type


class InteractionsAggregator(abc.ABC):

    def __init__(self, interaction_name: str):
        self.__name = interaction_name

    @property
    def name(self):
        """
        Returns:
            the type of interaction this object handles.
        """
        return self.__name

    @abc.abstractmethod
    def initialize_interactions_container(self) -> Container:
        """
        initialize the data-structure in which the found interactions are aggregated, between a pair of users.
        Returns:
            a mutable container data structure
        """
        raise NotImplemented

    @abc.abstractmethod
    def extract(self, node: N, branch: List[N], tree: N) -> Iterable[Tuple[Any, Any, T]]:
        """
        extract the interaction between any pair of users according to the given node in the tree.
        Args:
            node: the node from which the interaction should be extracted.
            branch: the branch preceding the 'node', from the root until the current 'node'.
            tree: the root of the whole conversation tree.

        Returns:
            an iterable of triplets (tuples with 3 elements) where:
                - the first element is the user_id of the user who made the interaction.
                - the second element is the user_id of the user who received the interaction.
                - the value of the interaction.
        """
        raise NotImplemented

    @abc.abstractmethod
    def add(self, u1: Any, u2: Any, interaction_value: T, container: Container):
        """
        adds the value of the interaction from user 'u1' to user 'u2' to the container.
        Args:
            u1: user id of the user that has made the interaction.
            u2: user id of the user that received the interaction.
            interaction_value: the value of the interaction.
            container: aggregates all of the interactions between theses pair of users.
        """
        raise NotImplemented

    @abc.abstractmethod
    def aggregate(self, container: Container) -> K:
        """
        takes the container that has aggregated the interactions between a pair of users,
        and transform it into the final interaction value between these users.
        Args:
            container: aggregates all of the interactions between theses pair of users.

        Returns:
            The final value that summarizes the interactions between
        """
        raise NotImplemented
