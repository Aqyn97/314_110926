# Advanced Parallel Programming Lab Answers

## Hardware Specs
* **CPU:** Apple M2 (8 physical cores: 4 Performance / 4 Efficiency, 8 logical cores)
* **L1 Data Cache:** 64 KB
* **L2 Cache:** 4 MB
* **Memory:** 8 GB LPDDR5
* **Memory Bandwidth:** 100 GB/s
* **Runtime:** Python 3

---

## Task 1: Amdahl’s Law

### Q1.1
My MacBook Air features 8 physical CPU cores (4 performance, 4 efficiency) and 8 logical cores, as Apple Silicon does not utilize SMT/hyperthreading. 

Using more than 8 workers leads to **oversubscription**, forcing the OS scheduler to context-switch threads over a fixed pool of hardware execution units. The experimental data reflects this: performance peaks at 8 workers and degrades as worker counts increase further.

### Q1.2
Given execution times of **1.8821 s** (1 worker) and **0.5471 s** (4 workers):

* **Observed Speedup:**
  $$S(4) = \frac{1.8821}{0.5471} \approx 3.44$$

* **Amdahl's Law Calculation:**
  $$S(N) = \frac{1}{(1 - P) + \frac{P}{N}}$$
  $$3.44 = \frac{1}{(1 - P) + \frac{P}{4}}$$
  $$1 - P + 0.25P = \frac{1}{3.44} \approx 0.2907$$
  $$0.75P \approx 0.7093 \implies P \approx 0.946$$

Approximately **94.6%** of the workload is parallelizable, leaving a serial bottleneck of **5.4%**.

### Q1.3
Scaling is sub-linear: peak speedup reached **4.70x** at 8 workers, compared to an ideal linear speedup of **8x**. 

Past 8 workers, execution time regressed (0.4668 s at 12 workers; 0.4936 s at 16 workers). Oversubscription overhead (context switching, thread management) combined with the non-parallelizable fraction $1 - P$ limits peak theoretical throughput.

---

## Task 2: False Sharing

### Q2.1
The adjacent allocation showed a marginal slowdown relative to the padded allocation across all three benchmark runs.

| Run | Adjacent (s) | Padded (s) |
| :--- | :---: | :---: |
| **Run 1** | 0.6407 | 0.6280 |
| **Run 2** | 0.6374 | 0.6319 |
| **Run 3** | 0.6307 | 0.6180 |
| **Median** | **0.6374** | **0.6280** |

$$\text{Median Slowdown Factor} = \frac{0.6374}{0.6280} \approx 1.01\text{x}$$

### Q2.2
False sharing occurs when independent variables accessed by different CPU cores reside on the same cache line. Even without logical data races, cache coherency protocols invalidate the entire cache line across cores whenever a write occurs, leading to excessive interconnect traffic ("cache ping-ponging"). Padding forces independent variables onto distinct cache lines, avoiding unnecessary invalidations.

### Q2.3
The performance impact (~1%) was lower than typically observed in low-level languages (like C/C++). This is largely due to CPython execution overhead and the high performance of Apple Silicon's L1/L2 cache coherency fabric. However, because the padded version was consistently faster across every run, the structural benefit of cache line isolation remains demonstrated.

---

## Task 3: Synchronization Tax vs. Lockless Design

### Q3.1
* **Unsafe Execution:** 0.0832 s
* **Locked Execution:** 0.2541 s

$$\text{Overhead Factor} = \frac{0.2541}{0.0832} \approx 3.06\text{x}$$

Acquiring and releasing locks introduces a ~3x slowdown. Furthermore, while the unsafe version executed faster, it introduces data races and lacks correctness guarantees under concurrent execution.

### Q3.2
* **Lockless Execution:** 0.0383 s (Correct count: 2,000,000)

$$\text{Speedup over Locked} = \frac{0.2541}{0.0383} \approx 6.63\text{x}$$

By eliminating shared state mutations during computation—using thread-local accumulators and aggregating them in a single step at completion—the lockless implementation bypasses synchronization overhead entirely.

### Q3.3
Synchronization imposes severe performance penalties when placed inside tight execution loops. The key architectural lesson is to structure concurrent algorithms around **thread-local state** to minimize contention, reserving shared synchronization only for final reductions or pipeline stages.

---

## Task 4: Roofline Model Analysis

### Q4.1
| Worker Count | Compute-Bound (s) | Memory-Bound (s) |
| :---: | :---: | :---: |
| **1** | 0.6014 | 0.3889 |
| **2** | 0.5767 | 0.4645 |
| **4** | 0.6381 | 0.8446 |

* **Compute-Bound:** Shows minimal variance between 1 and 2 workers, then regresses at 4 workers due to worker creation and management costs overriding pure compute throughput gains.
* **Memory-Bound:** Monotonically degrades as worker count increases (more than doubling in time at 4 workers) because memory access patterns exhaust available channel capacity.

### Q4.2
The Apple M2 features a system-wide unified memory architecture with **100 GB/s bandwidth** shared across CPU and GPU pipelines. In memory-saturated workloads, adding threads increases contention for memory bus access and cache lines without increasing total throughput, causing severe performance degradation.

### Q4.3
The operational ceiling of a workload dictates its parallel scalability:
* **Compute-bound** workloads scale until CPU pipelines are saturated or scheduling overhead dominates.
* **Memory-bound** workloads hit memory bandwidth walls early; adding parallel workers increases bus contention rather than speed, degrading execution efficiency.

---

## Bonus: Threading vs. Multiprocessing

### Inflection Point Analysis
* **Multiprocessing Performance:** Scaled efficiently up to 8 processes, matching hardware core count.
  * *1 Process:* 1.9785 s
  * *2 Processes:* 1.0837 s
  * *4 Processes:* 0.5979 s
  * *8 Processes:* 0.4664 s (Optimal)
  * *16 Processes:* 0.5171 s (Degradation)
  * *32 Processes:* 0.6926 s (Degradation)
* **Threading Performance:** Remained stagnant at ~2.0 seconds regardless of thread count (Best: 1.9658 s at 2 threads).

### Autopsy & Root Cause
The Global Interpreter Lock (**GIL**) in standard CPython prevents multiple native threads from executing Python bytecode simultaneously within a single process. Consequently, multi-threaded CPU-bound code runs serially on a single core.

Multiprocessing bypasses the GIL by spawning distinct CPython interpreter instances, enabling true parallel execution across all 8 CPU cores up to core saturation (8 workers). Past 8 processes, inter-process communication (IPC) and OS context-switching overhead begin to degrade throughput