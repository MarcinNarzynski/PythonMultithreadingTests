import asyncio
import time
from colorama import Fore as F


async def worker(input_data: dict[str, int], loop_count: int) -> None:
    for _ in range(loop_count):
        input_data["counter"] += 1


# Global variable used by all workers in parallel:
counter: dict[str, int] = {"counter": 0}


async def start_tasks(worker_count: int):
    workers = [worker(counter, 1_000_000) for _ in range(worker_count)]

    start = time.perf_counter()

    await asyncio.gather(*workers)

    timer = time.perf_counter() - start
    return timer


for idx in range(2, 51, 8):
    counter['counter'] = 0
    time_count = asyncio.run(start_tasks(idx))

    print(f"{F.CYAN}Number of workers: {idx}")
    print(f"  Counter value: {counter['counter']:,}")
    print(f"  Time: {time_count * 1000:.03f} ms")
    print(f"  {F.LIGHTYELLOW_EX}Time per worker: {time_count * 1000 / idx:.03f} ms")
