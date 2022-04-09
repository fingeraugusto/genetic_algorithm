from abc import ABC, abstractmethod
from itertools import zip_longest
from individual import Individual
from typing import List, Tuple
import random

def generate_random_int(low: int, upper: int) -> int:
    return random.randint(low, upper)

def k_tournament(k: int, n_individuals: int, pop: List[Individual]) -> List[int]:
    """Perform a k tournament, collectin champions up to the n_individual is reached.
    If the pool is empty, reset the candidates and continue. It return a list of int containing
    all the champions. A number of individuals greater than the population size is allowed.
    """
    # TODO: create or look for a doble linked list to speed up the pop function
    champions = []
    candidates_index = [i for i in range(len(pop))]
    
    while len(champions) < n_individuals:
        tournament = []
        tournament_ind = []

        # reset the candidates if there is not enough candidates
        if len(candidates_index) < k:
            candidates_index = [i for i in range(len(pop))]
        
        while len(tournament) <= k:
            new_index = generate_random_int(0, len(candidates_index) - 1)
            candidates_index.pop(new_index)
            tournament.append(new_index)
            tournament_ind.append(pop[new_index])
        
        final_candidates = [x for _, x in sorted(zip(tournament_ind, tournament))]
        champions.append(final_candidates[0])

    return champions

"""
BasePopulationSelector is used to select the final population, from the mutated children and the parents.

"""
# TODO: K_tournament for the selection
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

"""
BaseParentsSelector is used to select all the parents pairs required for the offsprin generation.

"""
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