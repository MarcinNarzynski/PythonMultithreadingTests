# Przykład mierzenia czasu wykonania pojedynczej funkcji z użyciem dekoratora
import math
import time


def measure_perf(function_under_test):
    def timed(*args, **kwargs):
        start = time.time()
        result = function_under_test(*args, **kwargs)
        end = time.time()

        print(f"Performance time of function '{function_under_test.__name__}' is:\n    {(end-start) * 1000:8.2f} ms")
        return result
    return timed


@measure_perf
def my_function():
    res = []
    for f in range(1000000):
        res.append(math.sin(f))
    return res


for i in range(10):
    result = my_function()
