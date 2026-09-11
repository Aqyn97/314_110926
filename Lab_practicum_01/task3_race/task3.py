import threading
import time

NUM_THREADS = 10
INCREMENTS_PER_THREAD = 1_000_000
EXPECTED = NUM_THREADS * INCREMENTS_PER_THREAD


class Counter:
    def __init__(self):
        self.value = 0


def worker_unlocked(counter: Counter):
    for _ in range(INCREMENTS_PER_THREAD):
        counter.value = counter.value + 1  # load -> add -> store, not atomic


def worker_locked(counter: Counter, lock: threading.Lock):
    for _ in range(INCREMENTS_PER_THREAD):
        with lock:
            counter.value = counter.value + 1


def run_unlocked_trial() -> int:
    counter = Counter()
    threads = [threading.Thread(target=worker_unlocked, args=(counter,))
               for _ in range(NUM_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter.value


def run_locked_timed() -> float:
    counter = Counter()
    lock = threading.Lock()
    threads = [threading.Thread(target=worker_locked, args=(counter, lock))
               for _ in range(NUM_THREADS)]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - t0
    assert counter.value == EXPECTED, "locked version should always be exact"
    return elapsed


def run_unlocked_timed() -> tuple[float, int]:
    counter = Counter()
    threads = [threading.Thread(target=worker_unlocked, args=(counter,))
               for _ in range(NUM_THREADS)]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - t0
    return elapsed, counter.value


def main():
    print(f"Expected total: {EXPECTED:,}\n")

    print("=== Q3 table: 10 unsynchronized runs ===")
    for i in range(1, 11):
        result = run_unlocked_trial()
        error = EXPECTED - result
        print(f"Run #{i:>2}: measured={result:,}  error={error:,}")

    print("\n=== Q3.2: timing comparison ===")
    unlocked_time, unlocked_result = run_unlocked_timed()
    print(f"Unlocked: {unlocked_time*1000:.1f} ms  (result={unlocked_result:,}, "
          f"{'CORRUPTED' if unlocked_result != EXPECTED else 'exact this time'})")

    locked_time = run_locked_timed()
    print(f"Locked:   {locked_time*1000:.1f} ms  (result={EXPECTED:,}, always exact)")
    print(f"\nSlowdown factor: {locked_time/unlocked_time:.2f}x")


if __name__ == "__main__":
    main()
