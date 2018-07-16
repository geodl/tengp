""" Tests for CMA-ES optimization method of CGP system """
import random
from time import time

from sklearn.metrics import mean_squared_error

from tengp import cma_es, Parameters

def test_cma_es_integration(function_set, input_data_1d):
    """ Test happy path for basic CMA-ES run """
    X, y = input_data_1d

    params = Parameters(1,1,1,3,function_set,use_tensorflow=False)

    random.seed(0)
    start = time()
    result = cma_es(X, y, mean_squared_error, params)

    print(f'CMA-ES result: {result}, time: {time() - start}')

    assert True, "passed without error"

