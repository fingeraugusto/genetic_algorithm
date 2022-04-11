import pytest
from typing import List
from genetic_algorithm.population import *
from genetic_algorithm.range import get_real_from_genes


def test_save_1(tmp_path):
    log_file = tmp_path / "mydir/log_file.txt"
    log_file.parent.mkdir() 
    log_file.touch()

    n_genes = 3
    n_ind = 100
    my_pop = Population(n_genes, n_ind, None)
    my_pop.set_log_file(str(log_file))
    my_pop.init_log()
    my_pop.pop[0].set_all_genes([0.12345,0.23456,0.0])
    my_pop.pop[0].set_fit_value(123456.1)
    my_pop.save_to_log()

    f = open(log_file, "r")
    aux = f.read()
    assert aux[-19:] == "0.12345,0.23456,0.0"

def test_load_1(tmp_path):
    log_file = tmp_path / "mydir/log_file.txt"
    log_file.parent.mkdir() 
    log_file.touch()
    log_file.write_text("fit:0.01      ,real_gen:1.1,1.23456,0.56790\n")

    n_genes = 3
    n_ind = 100
    my_pop = Population(n_genes, n_ind, None)
    my_pop.set_range({0:LinearRange(-10.0, 10.0), 1:LinearRange(-10.0, 10.0), 2:LinearRange(-10.0, 10.0)})
    my_pop.set_log_file(str(log_file))
    my_pop.init_log()

    aux = get_real_from_genes(my_pop.pop[0].genes(), my_pop.get_range_dict())
    aux[0] = round(aux[0],1)
    aux[1] = round(aux[1],5)
    aux[2] = round(aux[2],5)
    assert aux == [1.1, 1.23456, 0.56790]

def test_load_2(tmp_path):
    log_file = tmp_path / "mydir/log_file.txt"
    log_file.parent.mkdir() 
    log_file.touch()
    log_file.write_text("fit:0.01      ,real_gen:1.1,1.23456,0.56790\nfit:0.01      ,real_gen:2.1,2.23456,2.56790\nfit:0.01      ,real_gen:1.1,1.23456,0.56790\n")

    n_genes = 3
    n_ind = 100
    my_pop = Population(n_genes, n_ind, None)
    my_pop.set_range({0:LinearRange(-10.0, 10.0), 1:LinearRange(-10.0, 10.0), 2:LinearRange(-10.0, 10.0)})
    my_pop.set_log_file(str(log_file))
    my_pop.init_log()

    aux = get_real_from_genes(my_pop.pop[0].genes(), my_pop.get_range_dict())
    aux[0] = round(aux[0],1)
    aux[1] = round(aux[1],5)
    aux[2] = round(aux[2],5)
    assert aux == [1.1, 1.23456, 0.56790]

def test_load_3(tmp_path):
    log_file = tmp_path / "mydir/log_file.txt"
    log_file.parent.mkdir() 
    log_file.touch()
    log_file.write_text("fit:0.01      ,real_gen:1.1,1.23456,0.56790\nfit:0.01      ,real_gen:2.1,2.23456,2.56790\nfit:0.01      ,real_gen:1.1,1.23456,0.56790")

    n_genes = 3
    n_ind = 100
    my_pop = Population(n_genes, n_ind, None)
    my_pop.set_range({0:LinearRange(-10.0, 10.0), 1:LinearRange(-10.0, 10.0), 2:LinearRange(-10.0, 10.0)})
    my_pop.set_log_file(str(log_file))
    my_pop.init_log()

    aux = get_real_from_genes(my_pop.pop[0].genes(), my_pop.get_range_dict())
    aux[0] = round(aux[0],1)
    aux[1] = round(aux[1],5)
    aux[2] = round(aux[2],5)
    assert aux == [1.1, 1.23456, 0.56790]

def test_load_4(tmp_path):
    log_file = tmp_path / "mydir/log_file.txt"
    log_file.parent.mkdir() 
    log_file.touch()
    log_file.write_text("fit:0.01      ,real_gen:1.1,1.23456,0.56790\nfit:0.01      ,real_gen:2.1,2.23456,2.56790\nfit:0.01      ,real_gen:1.1,1.23456,0.56790\n\n")

    n_genes = 3
    n_ind = 100
    my_pop = Population(n_genes, n_ind, None)
    my_pop.set_range({0:LinearRange(-10.0, 10.0), 1:LinearRange(-10.0, 10.0), 2:LinearRange(-10.0, 10.0)})
    my_pop.set_log_file(str(log_file))
    my_pop.init_log()

    # assert my_pop.pop[0].genes() ==  my_pop.get_range_dict()
    aux = get_real_from_genes(my_pop.pop[0].genes(), my_pop.get_range_dict())
    aux[0] = round(aux[0],1)
    aux[1] = round(aux[1],5)
    aux[2] = round(aux[2],5)
    assert aux == [1.1, 1.23456, 0.56790]


class TestBenchmark:
    """
    benchmark_1  -> Three-hump camel, f(x,y) = 2x**2 - 1.05*x**4 + (1/6)*x**6 + x*y + y**2
                    Solution: f(0, 0) = 0.0 
    benchmark_2  -> Beale function, f(x,y) = (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2
                    Solution: f(3, 0.5) = 0
    benchmark_3  -> Rosenbrock function, f(*args) = sum(n-1){100*(x[i+1] - x[i]**2)**2 + (1 - x[i])**2}
                    Solution: f(1...1) = 0
    """
    
    def test_benchmark_1_small_range(self) -> None:
        def f (inputs: List[float]) -> float:
            x, y = inputs
            return 2*x**2 - 1.05*x**4 + (1/6)*x**6 + x*y + y**2
        
        n_genes = 2
        n_ind = 100
        my_pop = Population(n_genes, n_ind, f)
        fit_1, _, _ = my_pop.evolve(10000, target=0.001)

        my_pop = Population(n_genes, n_ind, f)
        fit_2, _, _ = my_pop.evolve(10000, target=0.001)
        assert min(fit_1, fit_2) <= 0.001


    def test_benchmark_1_large_range(self) -> None:
        def f (inputs: List[float]) -> float:
            x, y = inputs
            return 2*x**2 - 1.05*x**4 + (1/6)*x**6 + x*y + y**2
        
        n_genes = 2
        n_ind = 100
        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:LinearRange(-10.0, 10.0), 1:LinearRange(-10.0, 10.0)})
        fit_1, _, _ = my_pop.evolve(10000, target=0.001)

        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:LinearRange(-10.0, 10.0), 1:LinearRange(-10.0, 10.0)})
        fit_2, _, _ = my_pop.evolve(10000, target=0.001)
        assert min(fit_1, fit_2) <= 0.001    


    def test_benchmark_1_expo_range(self) -> None:
        def f (inputs: List[float]) -> float:
            x, y = inputs
            return 2*x**2 - 1.05*x**4 + (1/6)*x**6 + x*y + y**2
        
        n_genes = 2
        n_ind = 100
        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:ExponentialRange(-10.0, 10.0), 1:ExponentialRange(-10, 10.0)})
        fit_1, _, _ = my_pop.evolve(10000, target=0.001)

        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:ExponentialRange(-10.0, 10.0), 1:ExponentialRange(-10, 10.0)})
        fit_2, _, _ = my_pop.evolve(10000, target=0.001)
        assert min(fit_1, fit_2) <= 0.001 
    

    def test_benchmark_1_neg_range(self) -> None:
        def f (inputs: List[float]) -> float:
            x, y = inputs
            return 2*x**2 - 1.05*x**4 + (1/6)*x**6 + x*y + y**2
        
        n_genes = 2
        n_ind = 100
        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:NegativeExponentialRange(-10.0, 10.0), 1:NegativeExponentialRange(-10, 10.0)})
        fit_1, _, _ = my_pop.evolve(10000, target=0.001)

        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:NegativeExponentialRange(-10.0, 10.0), 1:NegativeExponentialRange(-10, 10.0)})
        fit_2, _, _ = my_pop.evolve(10000, target=0.001)
        assert min(fit_1, fit_2) <= 0.001
    

    def test_benchmark_2(self) -> None:
        def f (inputs: List[float]) -> float:
            x, y = inputs
            return (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2
        
        n_genes = 2
        n_ind = 100
        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:LinearRange(-4.5, 4.5), 1:LinearRange(-4.5, 4.5)})
        fit_1, _, _ = my_pop.evolve(10000, target=0.001)
        
        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({0:LinearRange(-4.5, 4.5), 1:LinearRange(-4.5, 4.5)})
        fit_2, _, _ = my_pop.evolve(10000, target=0.001)
        assert min(fit_1, fit_2) <= 0.001
    
    @pytest.mark.skip(reason="Too long")
    def test_benchmark_3(self) -> None:
        def f (inputs: List[float]) -> float:
            x = inputs
            sum = 0
            for i in range(len(x) - 1):
                sum += 100*(x[i+1] - x[i]**2)**2 + (1 - x[i])**2
            return sum
        
        fit = []
        n_ind = 100

        for n_genes in range(2, 15):
            my_pop = Population(n_genes, n_ind, f)
            my_pop.set_range({i:NegativeExponentialRange(-50.0, 50.0) for i in range(n_genes)})
            my_pop.log["gen_freq"] = 9999
            _fit, _, _ = my_pop.evolve(1000, target=0.1)
            fit.append(_fit)

        n_genes = 10
        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({i:LinearRange(-1000, 1000) for i in range(n_genes)})
        my_pop.log["gen_freq"] = 9999
        _fit, _, _ = my_pop.evolve(1000, target=0.1)
        fit.append(_fit)

        my_pop = Population(n_genes, n_ind, f)
        my_pop.set_range({i:LinearRange(-1000, 1000) for i in range(n_genes)})
        my_pop.set_models(crossover=SBXCrossover())
        my_pop.log["gen_freq"] = 9999
        _fit, _, _ = my_pop.evolve(1000, target=0.1)
        fit.append(_fit)

        assert min(fit) <= 1.0