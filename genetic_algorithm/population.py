from .individual import Individual, create_list_of_random_individuals
from .range import BaseRange, LinearRange, get_real_from_genes ,create_range_from_str
from .parent_selector import BaseParentsSelector, KTournamentParentSelector
from .population_selector import BasePopulationSelector, BestIndividualSelector
from .crossover import BaseCrossover, RandomCrossover
from .mutator import BaseMutator, AllRandom
from .stall import BaseStallControl, GenerationStallControl
from .save_load_print import DefaultLog
from math import inf
from typing import Callable, List, Dict, Tuple


class Population:
    def __init__(self, num_of_genes: int, num_of_individuals: int, fitness_fun: Callable[[List[float]], float], reverse: bool = False) -> None:
        self.num_of_genes = num_of_genes
        self.num_individuals = num_of_individuals
        self.reverse = reverse
        self.fitness_fun = fitness_fun
        
        self.__range = {i:LinearRange(0.0, 1.0) for i in range(self.num_of_genes)}
        self.__parent_selector = KTournamentParentSelector()
        self.__crossover = RandomCrossover()
        self.__mutator = AllRandom()
        self.__pop_selector = BestIndividualSelector()
        self.__stall = GenerationStallControl()
        self.__log = DefaultLog()
        self.log = {"print": True,
                    "gen_freq": 100,
                    "time_freq": 15,
                    "last_best": inf}
        self.pop = create_list_of_random_individuals( self.num_individuals, self.num_of_genes, reverse=self.reverse)

    def set_log_file(self, log_file: str) -> None:
        self.log["log_path"] = log_file
        if self.log["log_path"][-4:] != ".txt":
            self.log["log_path"] += ".txt"

    def set_models(self, parent_selector: BaseParentsSelector = None,
                        crossover: BaseCrossover = None,
                        mutator: BaseMutator = None,
                        pop_selector: BasePopulationSelector = None,
                        stall: BaseStallControl = None,
                        log: DefaultLog = None
                    ) -> None:
        if parent_selector:
            self.__parent_selector = parent_selector
        if crossover:
            self.__crossover = crossover
        if mutator:
            self.__mutator = mutator
        if pop_selector:
            self.__pop_selector = pop_selector
        if stall:
            self.__stall = stall
        if log:
            self.__log = log

    def set_range_from_dict(self, new_range: Dict[int, BaseRange]) -> None:
        """ gen_index:BaseRange """
        self.__range.update(new_range)
    
    def set_range_from_str(self, new_range: str) -> None:
        """ str_pattern:
        <index>:<type>(<lower>;<upper>;<optional>)
        More details look into range.create_range_from_str function
         """
        self.set_range_from_dict(create_range_from_str(new_range))
    
    def get_range_dict(self) -> Dict[int, BaseRange]:
        return self.__range
    
    def init_log(self) -> None:
        self.pop[0] = self.__log.init_log(self.pop, self.log, self.__range)

    def update_log(self, cur_gen: int, max_gen: int) -> None:
        self.__log.update_log(cur_gen, max_gen, self.pop)

    def save_to_log(self) -> None:
        self.__log.save_to_log(self.pop[0])

    def load_from_log(self) -> None:
        self.pop[0] = self.__log.load_from_log()
    
    def get_genes_from_real(self, list_of_real: List[float]) -> List[float]:
        return [self.__range[i].get_gene_from_real(real) for i, real in enumerate(list_of_real)]

    def calculate_fitness(self, ind: Individual) -> None:
        fit = self.fitness_fun(get_real_from_genes(ind.genes(), self.__range))
        ind.set_fit_value(fit)

    def calculate_all_fitness(self, pop: List[Individual]) -> None:
        for ind in pop:
            self.calculate_fitness(ind)
        pop.sort()

    def select_parents_pairs(self) -> List[Tuple[int, int]]:
        return self.__parent_selector.select_all_parents(self.pop)

    def crossover(self, parents_pair: List[Tuple[int, int]]) -> List[Individual]:
        return self.__crossover.generate_all_offspring(self.pop, parents_pair)

    def mutate(self, pop: List[Individual]) -> None:
        self.__mutator.mutate_all_individuals(pop)
    
    def select_next_pop(self, children_pop: List[Individual]) -> None:
        self.pop = self.__pop_selector.select_population(self.num_individuals, self.pop, children_pop)
    
    def stall_control(self, cur_gen: int, max_generation: int) -> int:
        return self.__stall.stall_pop(cur_gen, max_generation, self.pop)

    def evolve(self, max_generations: int, target: float = 0.0) -> Tuple[float, List[float], List[float]]:
        """Return a tuple containing (fitness_value, real_genes_list, gene_list)"""
        cur_gen = 0
        self.init_log()
        self.calculate_all_fitness(self.pop)

        while cur_gen < max_generations:
            cur_gen += 1

            children_pop = self.crossover(self.select_parents_pairs())
            self.mutate(children_pop)
            self.calculate_all_fitness(children_pop)
            self.select_next_pop(children_pop)
            self.update_log(cur_gen, max_generations)
            cur_gen = self.stall_control(cur_gen, max_generations)
            # to ensure all individulas have been evaluated
            self.calculate_all_fitness(self.pop)

            if self.pop[0].fit() <= target:
                return (self.pop[0].fit(), get_real_from_genes(self.pop[0].genes(), self.__range), self.pop[0].genes())

        return (self.pop[0].fit(), get_real_from_genes(self.pop[0].genes(), self.__range), self.pop[0].genes())

