from math import inf
from typing import List
from random import uniform

LOWER_GENE = 0.0
UPPER_GENE = 1.0
DEFAULT_FIT = inf

# TODO: IMPEDIR OPERAÇOES COM REQUIRED=TRUE
class Individual:
    def __init__(self, num_of_genes: int, list_of_genes: List[float] = [], reverse: bool = False) -> None:
        self.__num_of_genes = num_of_genes
        self.__list_of_genes = [0.0 for _ in range(self.__num_of_genes)]
        self.__fit = DEFAULT_FIT
        self.__require_update = True
        self.__reverse = reverse
        if list_of_genes:
            self.set_all_genes(list_of_genes)
        else:
            self.randomize_genes()

    def __str__(self) -> str:
        return f"(Individual) fit: {self.fit()}, genes: " + ",".join([str(g) for g in self.__list_of_genes])

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.fit() < other.fit()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.fit() <= other.fit()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.fit() == other.fit()

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.fit() != other.fit()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.fit() >= other.fit()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Individual):
            return NotImplemented
        return self.fit() > other.fit()

    def require_update(self) -> bool:
        return self.__require_update
    
    def fit(self) -> float:
        if self.require_update():
            if self.__reverse:
                return -DEFAULT_FIT
            return DEFAULT_FIT
        return self.__fit

    def get_num_of_genes(self) -> int:
        return self.__num_of_genes

    def gene(self, gene_index: int) -> float:
        return self.__list_of_genes[gene_index]

    def genes(self) -> List[float]:
        return self.__list_of_genes.copy()

    def set_new_gene_value(self, gene_index: int, new_value: float) -> None:
        self.__list_of_genes[gene_index] = max(min(new_value, UPPER_GENE), LOWER_GENE)
        self.__require_update = True
    
    def set_all_genes(self, new_genes_list: List[float]) -> None:
        if len(new_genes_list) != self.__num_of_genes:
            raise Exception(f"The new gene list has a different amount of parameters. Expected: {self.__num_of_genes}, found: {len(new_genes_list)}.")
        for g in range(self.__num_of_genes):
            self.set_new_gene_value(g, new_genes_list[g])

    def randomize_genes(self) -> None:
        for g in range(self.__num_of_genes):
            self.set_new_gene_value(g, uniform(LOWER_GENE, UPPER_GENE))
    
    def set_fit_value(self, new_fit_value: float) -> None:
        self.__fit = new_fit_value
        self.__require_update = False
    

def create_list_of_random_individuals(number_of_ind: int, number_of_genes: int, reverse: bool = False) -> List[Individual]:
    return [Individual(number_of_genes, reverse=reverse) for _ in range(number_of_ind)]