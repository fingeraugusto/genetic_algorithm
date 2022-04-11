# genetic_algorithm

My implementation of a Genetic Optimization. Uses an evolving function, with crossover, mutation and selection of the new generation.

## Example

The Population object is the responsible for performing all the evolution. Custom models for range, parent selection, cross over, mutator, population 
selection and a stall can be used instead.

The basic example requires only the definition of a callable fitness function as:

```python
from genetic_algorithm import *
my_pop = Populatiion(num_of_genes, num_of_individuals, fitness_function)
fit_value, best_values, genes = my_pop.evolve(num_of_generations)
```

Using the provided range objects allows for the model to provide the fitness function with a real value for the current gene, which is bounded to [0.0, 1.0].
The fitness function must be a callable object that accepts a list of floats with the same len of the number of genes and return a float as a result.

Currently, a basic save and load of genes is available. To use this functionalities, provide a .txt file path as
```python
my_pop.set_log_file(log_file_path)
```
The population will try to load the last entry before evolving. (Before mannually create your log file, check how the save is formatted by running a test example)

### Range

Range objects are  optional, but can be used to provide the proper transformation of the gene value from [0.0, 1.0] to the expeted values. When initializing
the Population, a dictionary containing the index of the gene (starting at 0) and the new model can be used to modify the default ones. Currently, three basic 
models are provided, being a LinearRange, an ExponentialRange and a NegativeExponentialRange. For small intervals, the LinearRange with custom intervals can
be quite useful. For problems with several orders of magnitude, The ExponentialRange models are the choice.

An example of usage can be observed below

```python
my_pop.set_range({0:LinearRange(-10.0, 10.0), 2:ExponentialRange(-10.0, 10.0), 3:NegativeExponentialRange(-10.0, 10.0, base=10)})
```
 There is no need to edit all the genes Range. If no model is provided for a gene index, the gene value will be provided to the fitness function. Both
 exponential models accpets a base parameter, if it is not provided, a `base=10` is used.
 
 ### Models
 
 Population accepts the configuration of several of it's models, and currently provided default implementations and abstract class for each one. To change
 a specific model, use:
```python
my_pop.set_models(parent_selector: BaseParentsSelector = None,
                  crossover: BaseCrossover = None,
                  mutator: BaseMutator = None,
                  pop_selector: BasePopulationSelector = None,
                  stall: BaseStallControl = None)
```

The current available models, starting with the default, are:
- parent_selector -> **selector.KTournamentParentSelector**
- crossover -> **crossover.RandomCrossover**, crossover.SBXCrossover
- mutator -> **mutator.AllRandom**
- pop_selector -> **selector.BestIndividualSelector**
- stall -> **stall.GenerationStallControl**

There are plnas to add more models as well as a custom save/load/print model. Additionally, a separation between the population and parents will be performed.
 
