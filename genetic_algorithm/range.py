from abc import ABC, abstractmethod
from typing import Tuple
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
