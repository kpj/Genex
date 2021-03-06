# Model Optimizer

Fit model of dynamical system to data


## Usage

```bash
$ python main.py LotkaVolterra result.pkl
$ python analyze_result.py result.pkl
```

## Tests

```bash
$ nosetests
```

## Presets

Exemplary function definitions can be found in `./presets/examples.py`.

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
  * Pause procedure and inspect generation with [CTRL]+[Z]
  * Optionally fix certain coefficients
* Fitness
  * Root relative squared error of series with multiple initial conditions
