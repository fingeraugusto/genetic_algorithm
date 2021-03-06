from abc import ABC, abstractmethod
from typing import Tuple, List, Dict
from .individual import LOWER_GENE, UPPER_GENE
import math

class BaseRange(ABC):
    """Framework to model range handlers"""
    @abstractmethod
    def get_real_from_gene(self, gene_value: float) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def get_gene_from_real(self, real_value: float) -> float:
        raise NotImplementedError


class LinearRange(BaseRange):
    """Uses a simple linear interpolation using (LOWER_GENE, lower_bound) and (UPPER_GENE, upper_bound)
    as (x0, y0) and (x1, y1). """
    def __init__(self, lower_bound: float, upper_bound: float, gen_range: Tuple[float, float] = (LOWER_GENE, UPPER_GENE)) -> None:
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.gen_range = gen_range
    
    def get_real_from_gene(self, gene_value: float) -> float:
        return self.lower_bound + (gene_value - self.gen_range[0]) * (self.upper_bound - self.lower_bound) / (self.gen_range[1] - self.gen_range[0])

    def get_gene_from_real(self, real_value: float) -> float:
        return self.gen_range[0] + (self.gen_range[1] - self.gen_range[0]) * (real_value - self.lower_bound) / (self.upper_bound - self.lower_bound)


class ExponentialRange(BaseRange):
    """Uses a linear interpolation with the points: (LOWER_GENE, lower_bound) and (UPPER_GENE, upper_bound), and 
    return the base to the power of the real value"""
    def __init__(self, lower_bound: float, upper_bound: float, base: float = 10.0, gen_range: Tuple[float, float] = (LOWER_GENE, UPPER_GENE)) -> None:
        self.__linear_helper = LinearRange(lower_bound, upper_bound, gen_range=gen_range)
        self.base = base
        self.gen_range = gen_range

    def get_real_from_gene(self, gene_value: float) -> float:
        return math.pow(self.base, self.__linear_helper.get_real_from_gene(gene_value))
         
    def get_gene_from_real(self, real_value: float) -> float:
        return self.__linear_helper.get_gene_from_real(math.log(real_value, self.base))


class NegativeExponentialRange(BaseRange):
    """Use a linear interpolation to obtain an exponent. If the gene is above UPPER_GENE / 2, interpolate
    between [UPPER_GENE / 2, UPPER_GENE] with the values [lower, upper] and return the pow(base, interpolaton). if the
    gene is below UPPER_GENE / 2, interpolate between [UPPER_GENE / 2, LOWER_GENE] with the values [lower, upper] and return the 
    -pow(base, interpolaton)"""
    def __init__(self, lower_bound: float, upper_bound: float, base: float = 10.0, gen_range: Tuple[float, float] = (LOWER_GENE, UPPER_GENE)) -> None:
        self.__linear_helper_positive = LinearRange(lower_bound, upper_bound, gen_range=(gen_range[1] / 2, gen_range[1]))
        self.__linear_helper_negative = LinearRange(lower_bound, upper_bound, gen_range=(gen_range[1] / 2, gen_range[0]))
        self.base = base
        self.gen_range = gen_range

    def get_real_from_gene(self, gene_value: float) -> float:
        if gene_value >= self.gen_range[1] / 2: # positive region
            return math.pow(self.base, self.__linear_helper_positive.get_real_from_gene(gene_value))
        return -math.pow(self.base, self.__linear_helper_negative.get_real_from_gene(gene_value))
        
    def get_gene_from_real(self, real_value: float) -> float:
        if real_value > 0:
            return self.__linear_helper_positive.get_gene_from_real(math.log(real_value, self.base))
        elif real_value < 0:
            return self.__linear_helper_negative.get_gene_from_real(math.log(- real_value, self.base))
        else:
            raise Exception("A zero real value was found for a NegativeExponentialRange.")


def get_real_from_genes(list_of_genes: List[float], range_dict: Dict[int, BaseRange]) -> List[float]:
        return [range_dict[i].get_real_from_gene(gen) for i, gen in enumerate(list_of_genes)]
    

def get_genes_from_real(list_of_real: List[float], range_dict: Dict[int, BaseRange]) -> List[float]:
    return [range_dict[i].get_gene_from_real(real) for i, real in enumerate(list_of_real)]


def create_range_from_str(range_str: str) -> Dict[int, BaseRange]:
    """
    Use it to inject the correct range without having to create the objects.
    the pattern follows:
    <index>:<type>(<lower>;<upper>;<optional>)
    separe each pattern with a comma.

    types:  L or l (linear, optional is ignored)
            E or e (exponential, if there is an optional, set the base=optional)
            N or n (negativeExponential, if there is an optional, set the base=optional)
    """
    range_dict = {}
    all_patterns = range_str.split(",")
    for p in all_patterns:
        g_idx, all_param = p.split(":")
        r_type, all_param = all_param[:,-1].split("(")
        all_param = all_param.split(";")
        new_range = None
        if r_type.lower() == "l":
            new_range = LinearRange(float(all_param[0], all_param[1]))
        elif r_type.lower() == "e":
            new_range = ExponentialRange(float(all_param[0], all_param[1]))
            if len(all_param == 3):
                new_range.base = float(all_param[2])
        elif r_type.lower() == "n":
            new_range = NegativeExponentialRange(float(all_param[0], all_param[1]))
            if len(all_param == 3):
                new_range.base = float(all_param[2])
        if new_range:
            range_dict[int(g_idx)] = new_range
    return range_dict
            

