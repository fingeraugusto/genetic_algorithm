from abc import ABC, abstractmethod
from .individual import Individual
from typing import List

class BasePopulationSelector(ABC):
    @abstractmethod
    def select_population(self, new_pop_size: int, pop_1: List[Individual], pop_2: List[Individual]) -> List[Individual]:
        raise NotImplementedError

class BestIndividualSelector(BasePopulationSelector):
    """Select the best n ind"""
    def select_population(self, new_pop_size: int, pop_1: List[Individual], pop_2: List[Individual]) -> List[Individual]:
        aux = [*pop_1, *pop_2]
        aux.sort()
        return aux[:new_pop_size]
