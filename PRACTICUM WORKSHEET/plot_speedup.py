import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("results.csv")))
t_seq = float([r for r in rows if r["mode"] == "seq"][0]["avg_s"])

# Table 1 rows = par + static + chunk 0 (first occurrence per thread count)
scal = {}
for r in rows:
    if r["mode"] == "par" and r["sched"] == "static" and r["chunk"] == "0":
        scal.setdefault(int(r["threads"]), float(r["avg_s"]))
ks = sorted(scal)

s_emp = {k: t_seq / scal[k] for k in ks}
p = 2 * (1 - 1 / s_emp[2])                       # derived from k=2
s_theo = {k: 1 / ((1 - p) + p / k) for k in ks}

print(f"T_seq = {t_seq:.4f} s   p = {p:.4f}")
print("k, T_k, S_emp, S_theo, Delta")
for k in ks:
    print(f"{k}, {scal[k]:.4f}, {s_emp[k]:.3f}, {s_theo[k]:.3f}, {s_theo[k]-s_emp[k]:.3f}")

plt.figure(figsize=(8, 5), dpi=200)
plt.plot(ks, ks, "k--", label="Linear ideal")
plt.plot(ks, [s_theo[k] for k in ks], "b-o", label=f"S_theo (Amdahl, p={p:.3f})")
plt.plot(ks, [s_emp[k] for k in ks], "r-s", label="S_emp")
plt.xlabel("Threads k"); plt.ylabel("Speedup")
plt.title("Amdahl Reality Gap"); plt.grid(alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig("speedup_plot.png")
