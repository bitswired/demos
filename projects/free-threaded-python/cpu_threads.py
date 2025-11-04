import threading
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


def run_threads(n):
    start = time.time()
    threads = []
    for _ in range(n):
        t = threading.Thread(target=cpu_task)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return time.time() - start


n = 4
print("Sequential CPU time:", run_sequential(n))
print("Threaded CPU time:", run_threads(n))
