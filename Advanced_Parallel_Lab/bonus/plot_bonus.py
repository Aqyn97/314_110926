"""
Optional: python3 plot_bonus.py
Needs matplotlib: pip3 install matplotlib --break-system-packages
"""
import csv
import matplotlib.pyplot as plt

workers, thread_times, proc_times = [], [], []

with open("bonus_results.csv") as f:
    for row in csv.DictReader(f):
        workers.append(int(row["workers"]))
        thread_times.append(float(row["threading_s"]))
        proc_times.append(float(row["multiprocessing_s"]))

plt.plot(workers, thread_times, marker="o", label="threading.Thread")
plt.plot(workers, proc_times, marker="o", label="multiprocessing.Pool")
plt.xlabel("Workers (T)")
plt.ylabel("Execution Time (s)")
plt.title("Threading vs Multiprocessing Scaling")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("bonus_scaling_curve.png", dpi=150)
print("Saved bonus_scaling_curve.png")
