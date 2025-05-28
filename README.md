
# Simulating and Analyzing Deadlock and Memory Allocation Strategies in Operating Systems

This project simulates memory allocation strategies—First Fit, Best Fit, Worst Fit—and implements the Banker's Algorithm to analyze system resource allocation, detect deadlocks, and evaluate overall memory performance. Visual outputs such as fragmentation comparison, execution time, resource allocation graphs, and safe sequences are generated for intuitive understanding.

---

## Members:
- De Justo, Izzy O.
- Fabul, Nathaniel C.
- Guiaya, Angelito Louise O.
- Semifrania, Joshua Jehiel M.
- Villarico, Lorenzo Noel A.

---

## Installation

Ensure Python is installed on your machine. Install required libraries using pip:

```bash
pip install matplotlib networkx
```

---

## Banker's Algorithm

```python
process_sequence = list(range(num_process))
arranged_sequence = []

k = 0
while k < len(max_need):
    if available + currently_holding[k] >= max_need[k]:
        available += currently_holding[k]
        arranged_sequence.append('P' + str(process_sequence[k] + 1))
        max_need.pop(k)
        currently_holding.pop(k)
        process_sequence.pop(k)
        k = 0
    else:
        k += 1
```

The Banker's Algorithm checks for a safe sequence of process execution without causing a deadlock. It calculates the available resources and iteratively determines whether each process can safely execute to completion. If a deadlock is detected, the system halts the simulation and outputs the blocked processes.

![Banker's Algorithm Gantt Chart](banker_algo.png)

---

## Memory Allocation Algorithms

### First Fit Strategy

```python
def first_fit(blocks, procs):
    alloc = [-1] * len(procs)
    mem = blocks.copy()
    frag = 0

    for i, p in enumerate(procs):
        for j, b in enumerate(mem):
            if b >= p:
                alloc[i] = j
                frag += b - p
                mem[j] -= p
                break
    return alloc, mem, frag
```

The First Fit strategy allocates the first memory block that is large enough for the process. It is straightforward and fast but can lead to memory fragmentation.

![First Fit RAG](first_fit.png)

---

### Worst Fit Strategy

```python
def worst_fit(blocks, procs):
    alloc = [-1] * len(procs)
    mem = blocks.copy()
    frag = 0

    for i, p in enumerate(procs):
        worst_idx = -1
        max_left = -1
        for j, b in enumerate(mem):
            if b >= p and b - p > max_left:
                worst_idx = j
                max_left = b - p
        if worst_idx != -1:
            alloc[i] = worst_idx
            frag += mem[worst_idx] - p
            mem[worst_idx] -= p
    return alloc, mem, frag
```

The Worst Fit strategy allocates the process to the largest available memory block. This aims to reduce the creation of small unusable fragments.

![Worst Fit RAG](worst_fit.png)

---

### Best Fit Strategy

```python
def best_fit(blocks, procs):
    alloc = [-1] * len(procs)
    mem = blocks.copy()
    frag = 0

    for i, p in enumerate(procs):
        best_idx = -1
        min_left = float('inf')
        for j, b in enumerate(mem):
            if b >= p and (b - p) < min_left:
                best_idx = j
                min_left = b - p
        if best_idx != -1:
            alloc[i] = best_idx
            frag += mem[best_idx] - p
            mem[best_idx] -= p
    return alloc, mem, frag
```

The Best Fit strategy finds the memory block that leaves the smallest leftover space after allocation, reducing overall fragmentation but potentially increasing search time.

![Best Fit RAG](best_fit.png)

---

## Performance of the Strategies

This section compares the three strategies based on fragmentation and execution time.

![Fragmentation and Execution Time Comparison](performance.png)

---

## Notes

- All graphs and charts are generated using `matplotlib` and `networkx`.
- Each memory allocation strategy also visualizes a Resource Allocation Graph (RAG) to illustrate allocation and request states.
- The safe sequence Gantt chart visually explains the outcome of the Banker's Algorithm.
