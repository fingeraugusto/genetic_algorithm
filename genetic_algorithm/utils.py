import random
from .individual import Individual
from typing import List


def generate_random_int(low: int, upper: int) -> int:
    return random.randint(low, upper)


def generate_random_number() -> float:
    return random.uniform(0.0, 1.0)


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