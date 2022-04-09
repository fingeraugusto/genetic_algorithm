from abc import ABC, abstractmethod
import math
from .individual import Individual
from typing import List

class BaseStallControl(ABC):
    """Framework to model stall controllers. The function return a cur_generation, most useful to run twin
    populations and ensure the total number of generations.
    """
    # TODO: use *args
    @abstractmethod
    def stall_pop(self, cur_generation: int, max_generations: int, pop: List[Individual]) -> int:
        raise NotImplementedError


class GenerationStallControl(BaseStallControl):
    def __init__(self, num_of_generations: int = 100, ind_ratio: float = 0.3) -> None:
        self.num_of_generations = num_of_generations
        self.ind_ratio = ind_ratio

    def stall_pop(self, cur_generation: int, max_generations: int, pop: List[Individual]) -> int:
        if cur_generation % self.num_of_generations == 0:
            for i in range(-1, -math.ceil(len(pop)*self.ind_ratio), -1):
                pop[i].randomize_genes()
        return cur_generation