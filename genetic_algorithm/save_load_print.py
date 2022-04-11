from abc import ABC, abstractmethod
import math

from genetic_algorithm.range import BaseRange, get_real_from_genes, get_genes_from_real
from .individual import Individual
from typing import Dict, List


class BaseSaveLoadPrint(ABC):
    @abstractmethod
    def init_log(self, list_of_individuals: List[Individual], log_file: str ="", log_config: Dict[str, str] = {}) -> Individual:
        raise NotImplementedError

    @abstractmethod
    def update_log(self, gen: int, max_gen: int,  list_of_individuals: List[Individual]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def save_to_log(self, ind: Individual) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_from_log(self) -> Individual:
        raise NotImplementedError


class DefaultLog(BaseSaveLoadPrint):
    def __init__(self) -> None:
        self.config = {}
        self.n_genes = 0
        self.last_best = math.inf
    
    def init_log(self, list_of_individuals: List[Individual], log_config: Dict[str, str], range_dict: Dict[int, BaseRange]) -> Individual:
        self.config = log_config
        self.range_dict = range_dict
        self.n_genes = list_of_individuals[0].get_num_of_genes()

        if self.config["print"]:
            print("======================================================================")
            print(" Start the evolution\n\n")
        
        return self.load_from_log()

    def update_log(self, gen: int, max_gen: int,  list_of_individuals: List[Individual]) -> None:
        if list_of_individuals[0].fit() < self.last_best:
            self.last_best = list_of_individuals[0].fit()
            self.save_to_log(list_of_individuals[0])
        self.print_log(gen, max_gen, list_of_individuals)

    def convert_individual_to_str(self, ind: Individual) -> str:
        ind_str = f"fit:{ind.fit():10.4e},real_gen:"
        return ind_str + ",".join([f"{r}" for r in get_real_from_genes(ind.genes(), self.range_dict)])
    
    def convert_str_to_individual(self, parsed_str: str) -> Individual:
        if not parsed_str:
            return Individual(self.n_genes)
        _ , real_genes = parsed_str.split("real_gen:")
        real_genes = [float(x) for x in real_genes.split(",")]
        return Individual(self.n_genes, list_of_genes=get_genes_from_real(real_genes, self.range_dict))
        
    def save_to_log(self, ind: Individual) -> None:
        if "log_path" in self.config:
            with open(self.config["log_path"], "a") as f:
                f.write(self.convert_individual_to_str(ind))

    def load_from_log(self) -> Individual:
        """Try to load a log file with a solution. If it succeeds, set the first individual with the genes loaded. """
        last_entry = ""
        if "log_path" in self.config:    
            with open(self.config["log_path"], "r") as f:
                all_lines = f.readlines()
                for i in range(-1, -(len(all_lines)+1), -1):
                    last_entry = all_lines[i].strip(" \n\r")
                    if last_entry:
                        break
        if last_entry:    
            return self.convert_str_to_individual(last_entry)
        return Individual(self.n_genes)

    def print_log(self, n_gen: int, max_gen: int, list_of_ind: List[Individual]) -> None:
        if self.config["print"]:
            if n_gen%self.config["gen_freq"] == 0:
                print("======================================================================")
                print(f" gen: {n_gen:<8}|| progress: {100*(n_gen/max_gen):3.2f}% " + 
                        f"|| cur_best: {list_of_ind[0].fit():10.2E} "+
                        f"|| cur_avg: {sum([x.fit() for x in list_of_ind]) / len(list_of_ind):10.2E}")
