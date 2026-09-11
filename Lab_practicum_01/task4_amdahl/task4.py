import argparse

N_TARGET = 64


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t1", type=float, required=True, help="measured N=1 avg time (s)")
    ap.add_argument("--t2", type=float, required=True, help="measured N=2 avg time (s)")
    args = ap.parse_args()

    t1, t2 = args.t1, args.t2

    p = 2 * (t1 - t2) / t1
    seq_fraction = 1 - p
    smax = 1 / seq_fraction if seq_fraction > 0 else float("inf")
    s64_amdahl = 1 / (seq_fraction + p / N_TARGET)
    s_gustafson = seq_fraction + p * N_TARGET

    print(f"T1 = {t1} s")
    print(f"T2 = {t2} s")
    print(f"Parallel fraction p        = {p:.4f}")
    print(f"Sequential fraction (1-p)  = {seq_fraction:.4f}")
    print(f"Amdahl max speedup (N->inf) = {smax:.2f}x")
    print(f"Amdahl speedup at N={N_TARGET}      = {s64_amdahl:.2f}x")
    print(f"Gustafson speedup at N={N_TARGET}   = {s_gustafson:.2f}x")


if __name__ == "__main__":
    main()
