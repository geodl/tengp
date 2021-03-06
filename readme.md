# TenGP - Cartesian Genetic Programming with NumPy (or PyTorch)

Cartesian Genetic Programming (CGP) based on NumPy arrays.

PyTorch tensors can be used instead of NumPy arrays, thanks to their similar APIs, thus enabling utilization of GPUs for transforming data.

## Installation

PyPI in progress. For know, installation is available only from git repo:
```
pip install git+https://github.com/Jarino/tengp
```

Or clone repo and install using Makefile:
```
git clone https://github.com/Jarino/tengp
cd tensor-cgp
make install
```


## Quick start

Symbolic regression example on [California Housing dataset](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html#sklearn.datasets.fetch_california_housing):

```python
# load data
from sklearn.datasets import fetch_california_housing

dataset = fetch_california_housing()
X_train = dataset.data
y_train = dataset.target

# set-up CGP system
import numpy as np
import tengp

def protected_division(x, y):
    return np.divide(x, y, out=np.copy(x), where=y!=0)

funset = tengp.FunctionSet()
funset.add(np.add, 2)
funset.add(np.subtract, 2)
funset.add(np.multiply, 2)
funset.add(protected_division, 2)
funset.add(np.sin, 1)

params = tengp.Parameters(n_inputs=X_train.shape[1],
                          n_outputs=1,
                          n_columns=100,
                          n_rows=1,
                          function_set=funset)

# cost function
from sklearn.metrics import mean_squared_error

# run evolution
res = tengp.simple_es(X_train,
                      y_train,
                      mean_squared_error,
                      params,
                      random_state=42,
                      mutation='probabilistic',
                      verbose=100)

# print fitness and phenotype of best individual
print(res[0].fitness)
print(res[0].get_expression())
```

## Features

Simple `$(1+n)$` evolution strategy using:
  - point mutation
  - single mutation
  - active mutation
  - probabilistic mutation

## Development

Install for development purposes:
```
make develop
```
which runs the `python setup.py develop` command.

If not installed, install `pytest` (`pip install pytest`), then:
```
make test
```

To build documentation:
```
make html
```
