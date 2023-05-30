import multiprocessing
from multiprocessing import Process, Queue
from time import time, sleep
import os
import math

INSIDE_LOOP = 7000
QUEUE_ELEMENTS = 1000  # Don't use to big queue - program hangs unless there is no consumer of output queue.

input_q = Queue()
output_q = Queue()


def calculate(loops, item):  # Some complicated calculations
    result = 0.0
    for f in range(loops):
        for d in item:
            result += math.sin(d / 10) * (f + 1) / 31415926

    return result


def worker(loops, input_q, output_q):
    worker_pid = os.getpid()
    # print("  Started worker no {}".format(worker_pid))

    # while not input_q.empty(): # This solution is invalid - not 100% certain
    while True:
        # print("Input queue size: {}".format(input_q.qsize()))
        item = input_q.get()
        if item is None:
            break

        calc = calculate(loops, item)
        output_q.put([int(item[0]), calc])  # Warning: too big output queue causes problems - program hangs during joining the subprocesses

    # print("    Finished worker no {}               ".format(worker_pid))


def consumer(output_q):
    consumer_pid = os.getpid()
    # print("  Started consumer no {}".format(consumer_pid))

    while True:
        try:
            result = output_q.get(timeout=0.5)
        except multiprocessing.queues.Empty:
            break
        # print("  Result: {}                    ".format(result), end='\r')
    # print("\n    Finished consumer no {}".format(consumer_pid))


def fill_input_data(number, input_q):
    print("\nPreparing input data...")

    start_time = time()
    for f in range(number):
        f = float(f + 1)
        input_q.put([f, 2*f, 3*f, 4*f, 5*f, 6*f, 7*f, 8*f, 9*f, 10*f])

    total_time = time() - start_time
    total_time *= 1000
    print("Input data prepared in {} ms.".format(round(total_time, 1)))
    print("Total elements in queue: {}.\n".format(input_q.qsize()))


def main_loop(number_of_workers):
    worker_processes = []

    fill_input_data(QUEUE_ELEMENTS, input_q)

    print(f"Starting workers number: {number_of_workers}")
    for w in range(number_of_workers):
        input_q.put(None)  # Added one 'None' per process to input queue at the end
        t = Process(target=worker, args=(INSIDE_LOOP, input_q, output_q))
        worker_processes.append(t)

    consumer_process = Process(target=consumer, args=(output_q,))

    start_time = time()

    for t in worker_processes:
        t.start()
    consumer_process.start()

    for t in worker_processes:
        t.join()  # Wait for every worker to finish his job
    consumer_process.join()

    total_time = time() - start_time
    # sleep(0.2)
    # print("\nProcessing time: {} s for workers number: {}".format(round(total_time, 3), number_of_workers))

    return total_time

    # while not output_q.empty():
    #     result = output_q.get()
    #     print(result)


if __name__ == '__main__':
    cpu_no = multiprocessing.cpu_count()
    print("Main program started.")
    print("Found {} cores in CPU.".format(cpu_no))

    results = []
    for number in range(1, cpu_no + 5):
    # for number in range(3, 5):
        result = [number, main_loop(number)]
        results.append(result)

    print("\nResults:")
    for r in results:
        print(f"  {r[0]:2}:  {r[1]:6.3f} s {results[0][1]/r[1]:6.2f} times faster")

    print("\nMain program finished.")