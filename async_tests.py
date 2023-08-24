import asyncio
import time
from asyncio import sleep
from dataclasses import dataclass
from functools import reduce
from random import random

from colorama import Fore as F


@dataclass
class Result:
    worker_id: int
    finished_time: float
    sum: int = 0


async def worker(worker_id: int, input_data: dict[str, int], loop_count: int) -> Result:
    for _ in range(loop_count):
        input_data["counter"] += 1
    await sleep(random())
    finished = round(time.perf_counter(), 3)
    print(f"{F.LIGHTBLUE_EX}Worker {worker_id} finished.")
    return Result(worker_id, finished, input_data["counter"])
    # return Result(worker_id, finished)


# Global variable used by all workers in parallel:
counter: dict[str, int] = {"counter": 0}
results = []


async def start_tasks(worker_count: int):
    global results
    workers = [worker(worker_id, counter, 1_000_000) for worker_id in range(worker_count)]
    start = time.perf_counter()
    results = await asyncio.gather(*workers)  # run all tasks and wait untill all finish the job
    timer = time.perf_counter() - start
    return timer


worker_count = 6
counter['counter'] = 0
time_count = asyncio.run(start_tasks(worker_count))

print(f"{F.CYAN}Number of workers: {worker_count}")
print(f"Counter value: {counter['counter']:,}")
print(f"Time: {time_count * 1000:.03f} ms")
print(f"{F.LIGHTYELLOW_EX}Time per worker: {time_count * 1000 / worker_count:.03f} ms")
print(f"{F.CYAN}{results}")

sorted_results = []

total = len(results)
for i in range(total):
    min_result = reduce(lambda x, y: x if x.finished_time <= y.finished_time else y, results)
    idx = results.index(min_result)
    # print(f"{F.LIGHTYELLOW_EX}{i} {idx} {min_result}")
    element = results.pop(idx)
    sorted_results.append(element)

print(f"{F.LIGHTYELLOW_EX}Sorted results:\n{sorted_results}")
