from individual import Individual
from range import *
from selector import *
from crossover import *
from mutator import *
from stall import *
from math import inf
from typing import Callable, List, Dict


def create_list_of_random_individuals(number_of_ind: int, number_of_genes: int, reverse: bool = False) -> List[Individual]:
    return [Individual(number_of_genes, reverse=reverse) for _ in range(number_of_ind)]


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
        self.log = {"print": True,
                    "gen_freq": 100,
                    "time_freq": 15,
                    "last_best": inf}
        self.pop = create_list_of_random_individuals( self.num_individuals, self.num_of_genes, reverse=self.reverse)

    def set_log_file(self, log_file: str) -> None:
        self.log["log_path"] = log_file
        if self.log["log_path"][-4:] != ".txt":
            self.log["log_path"] += ".txt"

    def set_parent_selector(self, new_model: BaseParentsSelector) -> None:
        self.__parent_selector = new_model

    def set_models(self, parent_selector: BaseParentsSelector = None,
                        crossover: BaseCrossover = None,
                        mutator: BaseMutator = None,
                        pop_selector: BasePopulationSelector = None,
                        stall: BaseStallControl = None
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
            self.__stall

    def set_range(self, new_range: Dict[int, BaseRange]) -> None:
        """ Accepted the str(gen_index) as the name parameter and a Range object as value. """
        self.__range.update(new_range)
    
    def convert_individual_to_str(self, ind: Individual) -> str:
        """ Return the representation of the individual with the real values. Use for save and load."""
        ind_str = f"fit:{ind.fit():10.4e},real_gen:"
        return ind_str + ",".join([f"{r}" for r in self.get_real_from_genes(ind.genes())])
    
    def convert_str_to_individual(self, parsed_str: str) -> Individual:
        if not parsed_str:
            return Individual(self.num_of_genes)
        _ , real_genes = parsed_str.split("real_gen:")
        real_genes = [float(x) for x in real_genes.split(",")]
        return Individual(self.num_of_genes, list_of_genes=self.get_genes_from_real(real_genes))
        
    def save_to_log(self) -> None:
        if "log_path" in self.log:
            with open(self.log["log_path"], "a") as f:
                f.write(self.convert_individual_to_str(self.pop[0]))

    def load_from_log(self) -> None:
        """Try to load a log file with a solution. If it succeeds, set the first individual with the genes loaded. """
        if "log_path" in self.log:
            last_entry = ""
            with open(self.log["log_path"], "r") as f:
                all_lines = f.readlines()
                for i in range(-1, -(len(all_lines)+1), -1):
                    last_entry = all_lines[i].strip(" \n\r")
                    if last_entry:
                        break
            self.pop[0] = self.convert_str_to_individual(last_entry)

    def print_log(self, n_gen: int, max_gen: int) -> None:
        if self.log["print"]:
            if n_gen == 0:
                print("======================================================================")
                print(" Start the evolution\n\n")
            else:
                if n_gen%self.log["gen_freq"] == 0:
                    print("======================================================================")
                    print(f" gen: {n_gen:<8}|| progress: {100*(n_gen/max_gen):3.2f}% " + 
                            f"|| cur_best: {self.pop[0].fit():10.2E} "+
                            f"|| cur_avg: {sum([x.fit() for x in self.pop]) / self.num_individuals:10.2E}")

    def get_real_from_genes(self, list_of_genes: List[float]) -> List[float]:
        return [self.__range[i].get_real_from_gene(gen) for i, gen in enumerate(list_of_genes)]
    
    def get_genes_from_real(self, list_of_real: List[float]) -> List[float]:
        return [self.__range[i].get_gene_from_real(real) for i, real in enumerate(list_of_real)]

    def calculate_fitness(self, ind: Individual) -> None:
        fit = self.fitness_fun(self.get_real_from_genes(ind.genes()))
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
        self.load_from_log()
        self.print_log(cur_gen, max_generations)
        self.calculate_all_fitness(self.pop)

        while cur_gen < max_generations:
            cur_gen += 1

            children_pop = self.crossover(self.select_parents_pairs())
            self.mutate(children_pop)
            self.calculate_all_fitness(children_pop)
            self.select_next_pop(children_pop)
            self.save_to_log()
            self.print_log(cur_gen, max_generations)
            cur_gen = self.stall_control(cur_gen, max_generations)
            # to ensure all individulas have been evaluated
            self.calculate_all_fitness(self.pop)

            if self.pop[0].fit() <= target:
                return (self.pop[0].fit(), self.get_real_from_genes(self.pop[0].genes()), self.pop[0].genes())

        return (self.pop[0].fit(), self.get_real_from_genes(self.pop[0].genes()), self.pop[0].genes())

