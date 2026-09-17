"""
Bonus Task: threading vs multiprocessing scaling curve.

The cpu_work() function below is copy-pasted unchanged, as instructed.
Everything else here is the harness needed to actually run it across
T in [1, 2, 4, 8, 16, 32] for both threading.Thread and
multiprocessing.Pool, and save the results so you can graph them.
"""
import csv
import time
from multiprocessing import Pool
import threading


def cpu_work(n):
    # Pure CPU crunch
    count = 0
    for i in range(n):
        count += i * i
    return count


TOTAL_WORK = 50_000_000
THREAD_COUNTS = [1, 2, 4, 8, 16, 32]


def run_multiprocessing(t):
    chunk = TOTAL_WORK // t
    start = time.perf_counter()
    with Pool(processes=t) as pool:
        pool.map(cpu_work, [chunk] * t)
    return time.perf_counter() - start


def run_threading(t):
    chunk = TOTAL_WORK // t
    threads = [threading.Thread(target=cpu_work, args=(chunk,)) for _ in range(t)]
    start = time.perf_counter()
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    return time.perf_counter() - start


if __name__ == "__main__":
    rows = []
    print(f"{'Workers':>8} | {'Threading (s)':>14} | {'Multiprocessing (s)':>20}")
    print("-" * 50)
    for t in THREAD_COUNTS:
        thread_time = run_threading(t)
        proc_time = run_multiprocessing(t)
        rows.append({"workers": t, "threading_s": thread_time, "multiprocessing_s": proc_time})
        print(f"{t:>8} | {thread_time:>14.4f} | {proc_time:>20.4f}")

    with open("bonus_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["workers", "threading_s", "multiprocessing_s"])
        writer.writeheader()
        writer.writerows(rows)
    print("\nSaved bonus_results.csv - import into Excel/Numbers/Sheets to plot,")
    print("or run plot_bonus.py if you have matplotlib installed.")
