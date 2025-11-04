# Free-Threaded Python

A demonstration of Python's new free-threaded mode (PEP 703) that allows true parallel execution by removing the Global Interpreter Lock (GIL). This project compares CPU-bound task performance with and without the GIL, as well as using multiprocessing.

📹 [Watch the video tutorial](https://youtu.be/p2wRL9ovI9o)

## Project Overview

This project demonstrates the performance differences between:
- Sequential execution
- Multi-threaded execution with GIL (traditional Python behavior)
- Multi-threaded execution without GIL (free-threaded mode)
- Multi-process execution

Python 3.13+ introduces experimental support for running without the Global Interpreter Lock, enabling true parallel execution of Python threads for CPU-bound tasks.

## Prerequisites

- Python 3.13 or higher (this project uses Python 3.14)
- `uv` package manager

## Installation

```bash
uv sync
```

## Usage

### Running with Free-Threaded Mode (No GIL)

To run Python without the GIL and experience true parallel thread execution:

```bash
PYTHON_GIL=0 uv run cpu_threads.py
```

### Running with Traditional GIL

To run Python with the GIL enabled (traditional behavior):

```bash
PYTHON_GIL=1 uv run cpu_threads.py
```

### Running with Multiprocessing

To compare with multiprocessing approach:

```bash
uv run cpu_processes.py
```

## How It Works

### cpu_threads.py

This script demonstrates the difference between sequential and multi-threaded execution of CPU-bound tasks:

- **cpu_task()**: Performs a CPU-intensive calculation (summing numbers from 0 to 10 million)
- **run_sequential(n)**: Runs the task n times sequentially
- **run_threads(n)**: Runs the task n times using separate threads

The performance difference between `PYTHON_GIL=0` and `PYTHON_GIL=1` clearly shows the impact of the GIL on parallel execution.

### cpu_processes.py

This script uses multiprocessing instead of threading to achieve parallelism:

- **run_processes(n)**: Runs the task n times using separate processes

Multiprocessing bypasses the GIL by using separate Python interpreters, but has higher overhead due to process creation and inter-process communication.

## Expected Results

- **With GIL (PYTHON_GIL=1)**: Threaded execution will be similar to or slower than sequential due to GIL contention
- **Without GIL (PYTHON_GIL=0)**: Threaded execution should be significantly faster, approaching near-linear speedup with the number of CPU cores
- **Multiprocessing**: Should show parallel speedup but with higher overhead than free-threaded mode

## Key Concepts

- **GIL (Global Interpreter Lock)**: A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously
- **Free-Threaded Mode**: Python 3.13+ feature that allows running without the GIL, enabling true parallel execution
- **CPU-bound vs I/O-bound**: This demonstration focuses on CPU-bound tasks where the GIL has the most impact

## Notes

- Free-threaded mode is experimental in Python 3.13/3.14
- Not all Python packages are compatible with free-threaded mode yet
- The `PYTHON_GIL` environment variable controls whether the GIL is enabled
- For I/O-bound tasks, threading already works well even with the GIL

## Resources

- [PEP 703 – Making the Global Interpreter Lock Optional](https://peps.python.org/pep-0703/)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)