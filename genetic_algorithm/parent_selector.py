from abc import ABC, abstractmethod
from .individual import Individual
from .utils import k_tournament
from typing import List, Tuple


class BaseParentsSelector(ABC):
    @abstractmethod
    def select_all_parents(self, parents: List[Individual]) -> List[Tuple[int, int]]:
        raise NotImplementedError

class KTournamentParentSelector(BaseParentsSelector):
    def __init__(self, k: int = 2, parents_ratio: float = 1.0) -> None:
        self.k = k
        self.parents_ratio = parents_ratio

    def select_all_parents(self, parents: List[Individual]) -> List[Tuple[int, int]]:
        all_parents = k_tournament(self.k, 2*round(self.parents_ratio * len(parents)), parents)
        parents_pair = []
        for i in range(0, len(all_parents), 2):
            if all_parents[i] != all_parents[i+1]:
                parents_pair.append((all_parents[i] , all_parents[i+1]))
        return parents_pair