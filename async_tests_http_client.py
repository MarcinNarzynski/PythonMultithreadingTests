import asyncio
import random
from asyncio import Queue

from aiohttp import ClientSession
from colorama import Fore as F

WORKERS_COUNT = 4
TASKS_COUNT = 15
TASK_GROUP = 5


class HttpClient:
    # https://docs.aiohttp.org/en/stable/client.html
    def __init__(self):
        self.session = ClientSession(base_url="http://httpbin.org")

    def __del__(self):
        # Solution for closing session from https://github.com/aio-libs/aiohttp/issues/2800
        if not self.session.closed:
            if self.session.connector_owner:
                self.session.connector.close()
            self.session._connector = None

    async def get_example_status(self, data: str):
        async with self.session.get("/get", ) as resp:
            status = resp.status

        return status


async def worker(worker_id: int, input_data: Queue, result_data: Queue, http_client: HttpClient) -> None:
    print(f"{F.LIGHTBLUE_EX}Worker {worker_id} started.")
    while True:
        to_do = await input_data.get()
        print(f"{F.LIGHTCYAN_EX}  Worker {worker_id} started processing task from queue...")

        status = await http_client.get_example_status(to_do)
        await result_data.put((to_do, status))

        await asyncio.sleep(random.random()*3 + 3)  # sleep 3-6 sec
        print(f"{F.GREEN}  Worker {worker_id} processed the request {to_do}")
        input_data.task_done()


async def main():
    input_data = Queue(maxsize=5)
    result_data = Queue()
    http_client = HttpClient()

    print(input_data)

    # Create fixed number of workers waiting for incoming tasks:
    workers = [asyncio.create_task(worker(worker_id=idx + 1, input_data=input_data, result_data=result_data, http_client=http_client), name="worker")
               for idx in range(WORKERS_COUNT)]

    await asyncio.sleep(1)  # not necessary, just to ensure workers are ready first, it must be a better way

    # Fill input data to make workers to process tasks:
    for idx in range(TASKS_COUNT):
        await input_data.put(f"{idx+1}: https://example.com")
        print(f"{F.LIGHTYELLOW_EX}Created input data no {idx + 1}")

    # Wait for workers to finish:
    await input_data.join()
    print(f"{F.LIGHTBLUE_EX}All workers finished")

    for w in workers:
        w.cancel()
    print(f"{F.LIGHTRED_EX}All workers stopped")

    print(f"{F.RESET}Results: {result_data}")


asyncio.run(main())
