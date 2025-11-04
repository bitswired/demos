import multiprocessing
import time


def cpu_task():
    result = 0
    for i in range(10**7):  # CPU-bound loop
        result += i
    return result


def run_sequential(n):
    start = time.time()
    for _ in range(n):
        cpu_task()
    return time.time() - start


def run_processes(n):
    start = time.time()
    processes = []
    for _ in range(n):
        t = multiprocessing.Process(target=cpu_task)
        t.start()
        processes.append(t)
    for p in processes:
        p.join()
    return time.time() - start


if __name__ == "__main__":
    n = 4
    print("Sequential CPU time:", run_sequential(n))
    print("Threaded CPU time:", run_processes(n))
