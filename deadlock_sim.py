import matplotlib.pyplot as plt
import time
import random
import networkx as nx

# -----------------------------
# Memory Allocation Strategies
# -----------------------------
processes = [10, 20, 30, 40, 50, 60]
 
memory_blocks = [15, 25, 35, 20] 


def first_fit(blocks, procs):
    alloc = [-1] * len(procs)
    mem = blocks.copy()
    frag = 0
    start = time.time()

    for i, p in enumerate(procs):
        for j, b in enumerate(mem):
            if b >= p:
                alloc[i] = j
                frag += b - p
                mem[j] -= p
                break

    exec_time = time.time() - start
    return alloc, mem, frag, exec_time


def best_fit(blocks, procs):
    alloc = [-1] * len(procs)
    mem = blocks.copy()
    frag = 0
    start = time.time()

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

    exec_time = time.time() - start
    return alloc, mem, frag, exec_time


def worst_fit(blocks, procs):
    alloc = [-1] * len(procs)
    mem = blocks.copy()
    frag = 0
    start = time.time()

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

    exec_time = time.time() - start
    return alloc, mem, frag, exec_time


def show_results(name, alloc, mem, frag):
    print(f"\n{name} Allocation:")
    for i, block in enumerate(alloc):
        if block != -1:
            print(f"Process {i} -> Block {block} ({memory_blocks[block]} -> Remaining: {mem[block]})")
        else:
            print(f"Process {i} -> Not Allocated")
    print(f"Total Fragmentation: {frag}")
    print(f"Remaining memory: {mem}")


# Run all strategies
ff_alloc, ff_mem, ff_frag, ff_time = first_fit(memory_blocks, processes)
bf_alloc, bf_mem, bf_frag, bf_time = best_fit(memory_blocks, processes)
wf_alloc, wf_mem, wf_frag, wf_time = worst_fit(memory_blocks, processes)

show_results("First Fit", ff_alloc, ff_mem, ff_frag)
show_results("Best Fit", bf_alloc, bf_mem, bf_frag)
show_results("Worst Fit", wf_alloc, wf_mem, wf_frag)

# -----------------------------
# Performance Comparison Plot
# -----------------------------
strategies = ['First Fit', 'Best Fit', 'Worst Fit']
frag_values = [ff_frag, bf_frag, wf_frag]
times = [ff_time, bf_time, wf_time]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Fragmentation plot
ax1.bar(strategies, frag_values, color='cornflowerblue')
ax1.set_title("Fragmentation Comparison")
ax1.set_ylabel("Total Fragmentation")
ax1.set_xlabel("Strategy")

# Execution time plot
ax2.bar(strategies, times, color='salmon')
ax2.set_title("Execution Time Comparison")
ax2.set_ylabel("Time (seconds)")
ax2.set_xlabel("Strategy")

plt.suptitle("Fragmentation & Execution Time")
plt.tight_layout()
plt.show()

# -----------------------------
# Resource Allocation Graph (RAG)
# -----------------------------
def draw_allocation_rag(strategy_name, alloc, mem_blocks):
    plt.title(f"Resource Allocation Graph - {strategy_name} Strategy", fontsize=18)
    processes = [f'P{i}' for i in range(len(alloc))]
    resources = [f'R{j}' for j in range(len(mem_blocks))]

    edges_alloc = []
    edges_req = []

    for i, block in enumerate(alloc):
        if block != -1:
            edges_alloc.append((f'R{block}', f'P{i}'))  # R -> P = allocated
        else:
            edges_req.append((f'P{i}', random.choice(resources)))  # P -> R = requesting

    G = nx.DiGraph()

    for p in processes:
        G.add_node(p, shape='circle', color='skyblue')
    for r in resources:
        G.add_node(r, shape='square', color='lightgreen')

    for (r, p) in edges_alloc:
        G.add_edge(r, p, color='red')  # Allocated: Red edge from R -> P
    for (p, r) in edges_req:
        G.add_edge(p, r, color='blue')  # Request: Blue edge from P -> R

    pos = nx.spring_layout(G, seed=42, k=1.5)
    node_colors = [G.nodes[n].get('color', 'gray') for n in G.nodes]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, arrows=True, font_size=14)
    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, arrows=True, arrowstyle='-|>', width=2)

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Process', markerfacecolor='skyblue', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Resource', markerfacecolor='lightgreen', markersize=10),
        plt.Line2D([0], [0], color='blue', lw=2, label='Requesting'),
        plt.Line2D([0], [0], color='red', lw=2, label='Allocated'),
    ]
    plt.legend(handles=legend_elements, fontsize=14)
    plt.tight_layout()
    plt.show()

draw_allocation_rag("First Fit", ff_alloc, memory_blocks)
draw_allocation_rag("Best Fit", bf_alloc, memory_blocks)
draw_allocation_rag("Worst Fit", wf_alloc, memory_blocks)

# -----------------------------
# Banker's Algorithm
# -----------------------------
print("\n\nBanker's Algorithm\n")

num_process = 10
available = 20

max_need = [7, 5, 3, 9, 4, 6, 10, 4, 3, 8]
currently_holding = [0, 1, 2, 3, 1, 2, 4, 0, 1, 3]

total = sum(currently_holding)
available -= total
print(f'Available resources: {available}')

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

if len(max_need) == 0:
    print('\nSafe sequence:', ' -> '.join(arranged_sequence))

    process_numbers = sorted([int(p[1:]) for p in arranged_sequence])
    y_labels = ['P' + str(i) for i in process_numbers]
    y_positions = {f'P{i}': idx for idx, i in enumerate(process_numbers)}

    fig, ax = plt.subplots(figsize=(8, len(y_labels) * 0.6))
    for i, proc in enumerate(arranged_sequence):
        y = y_positions[proc]
        ax.broken_barh([(i, 1)], (y - 0.4, 0.8), facecolors='skyblue')
        ax.text(i + 0.5, y, proc, va='center', ha='center', fontsize=12, color='black')

    ax.set_xlabel("Sequence Step")
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)
    ax.set_xticks(range(len(arranged_sequence)))
    ax.set_title("Banker's Algorithm - Gantt Chart of Safe Sequence (Sorted by Process ID)")
    ax.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("\nDeadlock Detected at step:", len(arranged_sequence))
    print("Processes in deadlock:", ['P' + str(i + 1) for i in process_sequence])
