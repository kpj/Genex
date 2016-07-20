# Model Optimizer

Fit model of dynamical system to data


## Usage

```
$ python main.py
```

## Tests

```
$ nosetests
```

## Features
* Initialization
  * Randomized individuals
* Selection
  * Fit individuals are more likely to be chosen for reproduction
* Crossover
  * Coefficient pulling
    * Randomized scale to prevent cycles
  * Coefficient sign switch
  * Exchange subtrees between terms
* Mutation
  * Add scaled Gauss to coefficient
  * Switch function with operator of same arity or different arity with randomized arguments
* Misc
  * Keep elite (fittest individuals) over generations
  * Apply culling technique
* Fitness
  * Least-squares of series with multiple initial conditions
