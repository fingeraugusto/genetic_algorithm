from abc import ABC, abstractmethod
from individual import Individual
from typing import List, Tuple
import random


def generate_random_number() -> float:
    return random.uniform(0.0, 1.0)


class BaseCrossover(ABC):
    @abstractmethod
    def generate_all_offspring(self, parents: List[Individual], parents_pair: List[Tuple[int, int]]) -> List[Individual]:
        raise NotImplementedError


class RandomCrossover(BaseCrossover):
    
    def __init__(self, children_ratio: float = 0.7) -> None:
        self.children_ration = children_ratio

    def generate_offspring(self, parent_1: Individual, parent_2: Individual) -> List[Individual]:
        children_1_genes = parent_1.genes()
        children_2_genes = parent_2.genes()
        n_genes = len(children_1_genes)
        count_crossovers = 0

        for i in range(n_genes):
            if generate_random_number() <= 0.5:
                count_crossovers += 1
                children_1_genes[i], children_2_genes[i] = children_2_genes[i], children_1_genes[i]
        # this ensures that at least one gene is swapped
        if count_crossovers == n_genes:
            children_1_genes[-1], children_2_genes[-1] = children_2_genes[-1], children_1_genes[-1]
        
        return [Individual(n_genes, list_of_genes=children_1_genes), Individual(n_genes, list_of_genes=children_2_genes)]

    def generate_all_offspring(self, parents: List[Individual], parents_pair: List[Tuple[int, int]]) -> List[Individual]:
        list_of_children = []
        for i in range(int(self.children_ration*len(parents_pair))):
            parent_1, parent_2  = parents[parents_pair[i][0]], parents[parents_pair[i][1]]
            list_of_children.extend(self.generate_offspring(parent_1, parent_2))
        return list_of_children


class SBXCrossover(BaseCrossover):
    """Based on https://stackoverflow.com/questions/22457941/simulated-binary-crossover-sbx-crossover-operator-example"""
    def __init__(self, n: float = 2.0, children_ratio: float = 0.7) -> None:
        self.n = n
        self.children_ratio = children_ratio

    def generate_offspring(self, parent_1: Individual, parent_2: Individual) -> List[Individual]:
        u = generate_random_number()
        if u < 0.5:
            b = (2*u)**(1 / (self.n + 1))
        else:
            b = (0.5 / (1 - u))**(1 / (self.n + 1))
        
        p_1 = parent_1.genes()
        p_2 = parent_2.genes()
        c_1 = [0.5*(1 + b)*p1 + (1 - b)*p2 for p1, p2 in zip(p_1,p_2)]
        c_2 = [0.5*(1 - b)*p1 + (1 + b)*p2 for p1, p2 in zip(p_1,p_2)]

        n_gen = len(p_1)
        return [Individual(n_gen, list_of_genes=c_1), Individual(n_gen, list_of_genes=c_2)]

    def generate_all_offspring(self, parents: List[Individual], parents_pair: List[Tuple[int, int]]) -> List[Individual]:
        list_of_children = []
        for i in range(int(self.children_ratio*len(parents_pair))):
            parent_1, parent_2  = parents[parents_pair[i][0]], parents[parents_pair[i][1]]
            list_of_children.extend(self.generate_offspring(parent_1, parent_2))
        return list_of_children

