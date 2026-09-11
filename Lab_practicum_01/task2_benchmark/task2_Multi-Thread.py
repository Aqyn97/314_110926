import argparse
import csv
import multiprocessing as mp
import time

from benchmark_core import count_primes_in_range

THREAD_COUNTS = [1, 2, 4, 8, 16, 32]
RUNS_PER_N = 3


def make_chunks(limit: int, n: int):
    """Split [2, limit) into n contiguous, roughly equal chunks."""
    step = (limit - 2) // n
    bounds = []
    start = 2
    for i in range(n):
        end = limit if i == n - 1 else start + step
        bounds.append((start, end))
        start = end
    return bounds


def run_once(limit: int, n: int) -> float:
    chunks = make_chunks(limit, n)
    t0 = time.perf_counter()
    with mp.Pool(processes=n) as pool:
        pool.map(count_primes_in_range, chunks)
    return time.perf_counter() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=3_000_000,
                     help="upper bound for prime counting workload")
    args = ap.parse_args()

    rows = []
    baseline_avg = None

    for n in THREAD_COUNTS:
        times = []
        for r in range(RUNS_PER_N):
            t = run_once(args.limit, n)
            times.append(t)
            print(f"N={n:>2}  run {r+1}/{RUNS_PER_N}: {t:.3f}s")
        avg = sum(times) / len(times)
        if n == 1:
            baseline_avg = avg
        speedup = baseline_avg / avg
        efficiency = speedup / n * 100
        rows.append({
            "N": n,
            "Run1_s": round(times[0], 3),
            "Run2_s": round(times[1], 3),
            "Run3_s": round(times[2], 3),
            "Avg_TN_s": round(avg, 3),
            "Speedup_SN": round(speedup, 3),
            "Efficiency_EN_pct": round(efficiency, 1),
        })

    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\n=== Markdown table for your report ===\n")
    print("| Threads (N) | Run1 (s) | Run2 (s) | Run3 (s) | Avg TN (s) | Speedup SN | Efficiency EN |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['N']} | {r['Run1_s']} | {r['Run2_s']} | {r['Run3_s']} | "
              f"{r['Avg_TN_s']} | {r['Speedup_SN']}x | {r['Efficiency_EN_pct']}% |")

    print(f"\nSaved raw data to results.csv")
    print(f"T1 (for Task 4) = {rows[0]['Avg_TN_s']} s")
    t2_row = next(r for r in rows if r["N"] == 2)
    print(f"T2 (for Task 4) = {t2_row['Avg_TN_s']} s")


if __name__ == "__main__":
    main()
