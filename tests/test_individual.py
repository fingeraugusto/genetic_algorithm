import pytest
from individual import *

class TestIndividual:
    
    # REQUIRED_UPDATE funcionality
    def test_require_update_one(self) -> None:
        individual_example = Individual(3)
        assert individual_example.require_update() == True

    def test_require_update_two(self) -> None:
        individual_example = Individual(3)
        individual_example.set_fit_value(1.0)
        assert individual_example.require_update() == False

    def test_require_update_three(self) -> None:
        individual_example = Individual(3)
        individual_example.set_fit_value(1.0)
        assert individual_example.require_update() == False

    # GENE MANIPULATION
    def test_gene_manipulation_one(self) -> None:
        individual_example = Individual(3)
        individual_example.set_new_gene_value(1, -2.0)
        assert individual_example.gene(1) == LOWER_GENE
    
    def test_gene_manipulation_two(self) -> None:
        individual_example = Individual(3)
        individual_example.set_new_gene_value(1, 2.0)
        assert individual_example.gene(1) == UPPER_GENE
    
    def test_gene_manipulation_three(self) -> None:
        individual_example = Individual(3)
        individual_example.set_all_genes([0.1, 0.2, 0.3])
        assert individual_example.genes() == [0.1, 0.2, 0.3]
    
    def test_wrong_size_of_genes(self) -> None:
        with pytest.raises(Exception):
            individual_example = Individual(3)
            individual_example.set_all_genes([0.1, 0.2, 0.3, 0.4])

    # INDIVIDUAL OPERATIONS
    def test_lt_fit(self) -> None:
        foo = Individual(3)
        foo.set_fit_value(1.0)
        bar = Individual(3)
        bar.set_fit_value(2.0)
        assert foo < bar
    
    def test_le_fit(self) -> None:
        foo = Individual(3)
        foo.set_fit_value(1.0)
        bar = Individual(3)
        bar.set_fit_value(1.0)
        assert foo <= bar
    
    def test_eq_fit(self) -> None:
        foo = Individual(3)
        foo.set_fit_value(1.0)
        bar = Individual(3)
        bar.set_fit_value(1.0)
        assert foo == bar
    
    def test_ne_fit(self) -> None:
        foo = Individual(3)
        foo.set_fit_value(1.0)
        bar = Individual(3)
        bar.set_fit_value(2.0)
        assert foo != bar

    def test_ge_fit(self) -> None:
        foo = Individual(3)
        foo.set_fit_value(1.0)
        bar = Individual(3)
        bar.set_fit_value(1.0)
        assert foo >= bar
    
    def test_gt_fit(self) -> None:
        foo = Individual(3)
        foo.set_fit_value(2.0)
        bar = Individual(3)
        bar.set_fit_value(1.0)
        assert foo > bar
