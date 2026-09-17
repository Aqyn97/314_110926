import threading
import time

TOTAL_OPS = 2_000_000
NUM_THREADS = 4


class UnsafeCounter:
    def __init__(self):
        self.val = 0

    def inc(self):
        self.val += 1


class LockedCounter:
    def __init__(self):
        self.val = 0
        self.lock = threading.Lock()

    def inc(self):
        with self.lock:
            self.val += 1


def bench(counter_type):
    c = counter_type()
    ops_per_thread = TOTAL_OPS // NUM_THREADS

    def work():
        for _ in range(ops_per_thread):
            c.inc()

    threads = [threading.Thread(target=work) for _ in range(NUM_THREADS)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return c.val, time.perf_counter() - start


# --- Lockless redesign (Q3.2): thread-local accumulation + single reduction ---
# Each thread only ever touches its own slot in `partial_sums`, so there's no
# shared mutable state during the hot loop and nothing to lock. We sum the
# partial results once, after all threads have finished.

def bench_lockless():
    ops_per_thread = TOTAL_OPS // NUM_THREADS
    partial_sums = [0] * NUM_THREADS

    def work(thread_id):
        local = 0  # keep it in a local var, not even touching the list, until the end
        for _ in range(ops_per_thread):
            local += 1
        partial_sums[thread_id] = local

    threads = [threading.Thread(target=work, args=(i,)) for i in range(NUM_THREADS)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    total = sum(partial_sums)  # reduction stage
    return total, elapsed


if __name__ == "__main__":
    val_unsafe, t_unsafe = bench(UnsafeCounter)
    val_locked, t_locked = bench(LockedCounter)
    val_lockless, t_lockless = bench_lockless()

    print(f"Unsafe:   Value = {val_unsafe:,} / {TOTAL_OPS:,} | Time: {t_unsafe:.4f}s")
    print(f"Locked:   Value = {val_locked:,} / {TOTAL_OPS:,} | Time: {t_locked:.4f}s")
    print(f"Lockless: Value = {val_lockless:,} / {TOTAL_OPS:,} | Time: {t_lockless:.4f}s")
    print(f"Contention Cost Multiplier (Locked/Unsafe): {t_locked / t_unsafe:.2f}x")
    print(f"Lockless Speedup vs Locked: {t_locked / t_lockless:.2f}x")
