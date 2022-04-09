from abc import ABC, abstractmethod
from .individual import Individual, UPPER_GENE
import random  
from typing import Callable, List
from .utils import generate_random_number

class BaseMutator(ABC):
    """Framework to model mutators handlers"""
    @abstractmethod
    def mutate_individual(self, individual: Individual) -> None:
        raise NotImplementedError

    @abstractmethod
    def mutate_all_individuals(self, list_individuals: List[Individual]) -> None:
        raise NotImplementedError


class AllRandom(BaseMutator):
    def __init__(self, ind_mut_chance: float = 0.05, gen_mut_chance: float = 0.1, mut_range: float = 0.1, random_generation_fun: Callable = generate_random_number) -> None:
        self.ind_mut_chance = ind_mut_chance
        self.gen_mut_chance = gen_mut_chance
        self.mut_range = mut_range
        self.random_fun = random_generation_fun
    

    def mutate_individual(self, individual: Individual) -> None:
        if self.random_fun() <= self.ind_mut_chance:
            new_genes = individual.genes()
            for i in range(len(new_genes)):
                if self.random_fun() <= self.gen_mut_chance:
                    new_genes[i] = new_genes[i] + (self.mut_range * UPPER_GENE) * (self.random_fun() - UPPER_GENE / 2)
            individual.set_all_genes(new_genes)

    def mutate_all_individuals(self, list_individuals: List[Individual]) -> None:
        for ind in list_individuals:
            self.mutate_individual(ind)
