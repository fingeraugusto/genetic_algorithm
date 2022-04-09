import pytest
from genetic_algorithm.range import *
import math

class TestLinearRange:
    # No range 
    def test_linear_real_from_gene_without_range_1(self) -> None:
        lin = LinearRange(0.0, 1.0)
        assert round(lin.get_real_from_gene(0.0), 1) == 0.0

    def test_linear_real_from_gene_without_range_2(self) -> None:
        lin = LinearRange(0.0, 1.0)
        assert round(lin.get_real_from_gene(0.25), 2) == 0.25

    def test_linear_real_from_gene_without_range_3(self) -> None:
        lin = LinearRange(0.0, 1.0)
        assert round(lin.get_real_from_gene(1.0), 1) == 1.0


    def test_linear_gene_from_real_without_range_1(self) -> None:
        lin = LinearRange(0.0, 1.0)
        assert round(lin.get_gene_from_real(0.0), 1) == 0.0

    def test_linear_gene_from_real_without_range_2(self) -> None:
        lin = LinearRange(0.0, 1.0)
        assert round(lin.get_gene_from_real(0.25), 2) == 0.25

    def test_linear_gene_from_real_without_range_3(self) -> None:
        lin = LinearRange(0.0, 1.0)
        assert round(lin.get_gene_from_real(1.0), 1) == 1.0

    # 0.0 - 10.0 range 
    def test_linear_real_from_gene_with_range_1(self) -> None:
        lin = LinearRange(0.0, 10.0)
        assert round(lin.get_real_from_gene(0.0), 1) == 0.0

    def test_linear_real_from_gene_with_range_2(self) -> None:
        lin = LinearRange(0.0, 10.0)
        assert round(lin.get_real_from_gene(0.25), 1) == 2.5

    def test_linear_real_from_gene_with_range_3(self) -> None:
        lin = LinearRange(0.0, 10.0)
        assert round(lin.get_real_from_gene(1.0), 1) == 10.0
    

    def test_linear_gene_from_real_with_range_1(self) -> None:
        lin = LinearRange(0.0, 10.0)
        assert round(lin.get_gene_from_real(0.0), 1) == 0.0

    def test_linear_gene_from_real_with_range_2(self) -> None:
        lin = LinearRange(0.0, 10.0)
        assert round(lin.get_gene_from_real(2.5), 2) == 0.25

    def test_linear_gene_from_real_with_range_3(self) -> None:
        lin = LinearRange(0.0, 10.0)
        assert round(lin.get_gene_from_real(10.0), 1) == 1.0

    # 1.0 - 0.0 range 
    def test_linear_real_from_gene_with_rev_range_1(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_real_from_gene(0.0), 1) == 1.0

    def test_linear_real_from_gene_with_rev_range_2(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_real_from_gene(0.25), 2) == 0.75

    def test_linear_real_from_gene_with_rev_range_3(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_real_from_gene(0.75), 2) == 0.25

    def test_linear_real_from_gene_with_rev_range_4(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_real_from_gene(1.0), 1) == 0.0
    
    
    def test_linear_gene_from_real_with_rev_range_1(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_gene_from_real(0.0), 1) == 1.0

    def test_linear_gene_from_real_with_rev_range_2(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_gene_from_real(0.25), 2) == 0.75

    def test_linear_gene_from_real_with_rev_range_3(self) -> None:
        lin = LinearRange(1.0, 0.0)
        assert round(lin.get_gene_from_real(1.0), 1) == 0.0


class TestExponentialRange:

    def test_expo_real_from_gene_1(self) -> None:
        test_base = 10.0
        gen = 0.0
        exp = ExponentialRange(0.0, 1.0, base=test_base)
        assert round(exp.get_real_from_gene(gen), 1) == round(math.pow(test_base, gen), 1)

    def test_expo_real_from_gene_2(self) -> None:
        test_base = 20.0
        gen = 1.0
        exp = ExponentialRange(0.0, 1.0, base=test_base)
        assert round(exp.get_real_from_gene(gen), 1) == round(math.pow(test_base, gen), 1)

    def test_expo_real_from_gene_3(self) -> None:
        test_base = 100.0
        gen = 0.5
        exp = ExponentialRange(0.0, 1.0, base=test_base)
        assert round(exp.get_real_from_gene(gen), 1) == round(math.pow(test_base, gen), 1)


    def test_expo_gene_from_real_1(self) -> None:
        test_base = 10.0
        gen = 0.0
        real = math.pow(test_base, gen)
        exp = ExponentialRange(0.0, 1.0, base=test_base)
        assert round(exp.get_gene_from_real(real), 1) == gen

    def test_expo_gene_from_real_2(self) -> None:
        test_base = 20.0
        gen = 1.0
        real = math.pow(test_base, gen)
        exp = ExponentialRange(0.0, 1.0, base=test_base)
        assert round(exp.get_gene_from_real(real), 1) == gen

    def test_expo_gene_from_real_3(self) -> None:
        test_base = 100.0
        gen = 0.5
        real = math.pow(test_base, gen)
        exp = ExponentialRange(0.0, 1.0, base=test_base)
        assert round(exp.get_gene_from_real(real), 1) == gen


class TestNegativeExponentialRange:

    def test_nexpo_real_from_gene_1(self) -> None:
        test_base = 10.0
        gen = 0.0
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_real_from_gene(gen), 1) == - round(math.pow(test_base, 1.0), 1)

    def test_nexpo_real_from_gene_2(self) -> None:
        test_base = 20.0
        gen = 1.0
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_real_from_gene(gen), 1) == round(math.pow(test_base, 1.0), 1)

    def test_nexpo_real_from_gene_3(self) -> None:
        test_base = 100.0
        gen = 0.5
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_real_from_gene(gen), 1) == round(math.pow(test_base, 0.0), 1)
    
    def test_nexpo_real_from_gene_4(self) -> None:
        test_base = 10.0
        gen = 0.75
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_real_from_gene(gen), 2) == round(math.pow(test_base, 0.5), 2)

    def test_nexpo_real_from_gene_5(self) -> None:
        test_base = 10.0
        gen = 0.25
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_real_from_gene(gen), 2) == - round(math.pow(test_base, 0.5), 2)


    def test_nexpo_gene_from_real_1(self) -> None:
        test_base = 10.0
        aux_gen = 0.0
        real = math.pow(test_base, aux_gen)
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_gene_from_real(real), 2) == round(aux_gen + 0.5, 2)

    def test_nexpo_gene_from_real_2(self) -> None:
        test_base = 10.0
        aux_gen = 1.0
        real = - math.pow(test_base, aux_gen)
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_gene_from_real(real), 2) == round(0, 2)

    def test_nexpo_gene_from_real_3(self) -> None:
        test_base = 10.0
        aux_gen = 0.5
        real = - math.pow(test_base, aux_gen)
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_gene_from_real(real), 2) == round(0.25, 2)

    def test_nexpo_gene_from_real_4(self) -> None:
        test_base = 10.0
        aux_gen = 0.5
        real = math.pow(test_base, aux_gen)
        nexp = NegativeExponentialRange(0.0, 1.0, base=test_base)
        assert round(nexp.get_gene_from_real(real), 2) == round(0.75, 2)