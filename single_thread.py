from math import sin
from time import time
from typing import List

results = []
start_time = time()
for it in range(1, 200000001):
    arg = it/10000.0
    # results.append(sin(arg)/arg)
    sinus = sin(arg)/arg

total_time_ms = (time() - start_time) * 1000

print(f"rozmiar tablicy: {len(results)/1000000} mln")
print(f"czas wykonania: {int(total_time_ms)} ms")
