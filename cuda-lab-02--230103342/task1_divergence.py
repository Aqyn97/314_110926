"""Task 1: Warp divergence microbenchmark (Kernel A uniform, B interleaved, C warp-aligned)."""
import time
import numpy as np
from numba import cuda

N = 2 ** 20            # 1,048,576 elements
ITERS = 1000           # iterations per element
THREADS_PER_BLOCK = 256
TRIALS = 10

# float32 constants keep all arithmetic in fp32 (python floats would promote to fp64)
MUL = np.float32(1.0001)
ADD = np.float32(0.0001)


@cuda.jit
def kernel_a_uniform(y, n, iters):
    """Every thread: y = y * 1.0001 + 0.0001, `iters` times."""
    idx = cuda.grid(1)
    if idx < n:
        v = y[idx]
        for _ in range(iters):
            v = v * MUL + ADD
        y[idx] = v


@cuda.jit
def kernel_b_interleaved(y, n, iters):
    """Even idx: multiply-accumulate. Odd idx: subtract-divide. Diverges inside every warp."""
    idx = cuda.grid(1)
    if idx < n:
        v = y[idx]
        if idx % 2 == 0:
            for _ in range(iters):
                v = v * MUL + ADD
        else:
            for _ in range(iters):
                v = (v - ADD) / MUL
        y[idx] = v


@cuda.jit
def kernel_c_warp_aligned(y, n, iters):
    """Branch on warp_id = idx // 32: whole warps take the same path (no intra-warp divergence)."""
    idx = cuda.grid(1)
    if idx < n:
        warp_id = idx // 32
        v = y[idx]
        if warp_id % 2 == 0:
            for _ in range(iters):
                v = v * MUL + ADD
        else:
            for _ in range(iters):
                v = (v - ADD) / MUL
        y[idx] = v


def benchmark(kernel, h_y, n=N, iters=ITERS, trials=TRIALS):
    """Kernel-only time in ms: 1 warm-up launch, then mean of `trials` timed launches.
    Host<->device copies happen OUTSIDE the timed region."""
    blocks = (n + THREADS_PER_BLOCK - 1) // THREADS_PER_BLOCK
    d_y = cuda.to_device(h_y)

    kernel[blocks, THREADS_PER_BLOCK](d_y, n, iters)   # warm-up (includes JIT compile)
    cuda.synchronize()

    times = []
    for _ in range(trials):
        d_y.copy_to_device(h_y)          # reset input (not timed)
        cuda.synchronize()
        t0 = time.perf_counter()
        kernel[blocks, THREADS_PER_BLOCK](d_y, n, iters)
        cuda.synchronize()
        times.append(time.perf_counter() - t0)
    return 1000.0 * sum(times) / len(times)


def main():
    dev = cuda.get_current_device()
    name = dev.name.decode() if isinstance(dev.name, bytes) else dev.name
    print(f"GPU: {name} | Compute Capability: {dev.compute_capability[0]}.{dev.compute_capability[1]}")

    h_y = np.ones(N, dtype=np.float32)
    results = {}
    for label, kern in (("A (Uniform)", kernel_a_uniform),
                        ("B (Full Divergence)", kernel_b_interleaved),
                        ("C (Warp-Aligned)", kernel_c_warp_aligned)):
        results[label] = benchmark(kern, h_y)
        print(f"Kernel {label}: {results[label]:.4f} ms")

    base = results["A (Uniform)"]
    print("\n| Kernel | Avg Kernel Time (ms) | Slowdown vs A |")
    print("|---|---|---|")
    for label, t in results.items():
        print(f"| {label} | {t:.4f} | {t / base:.2f}x |")
    print(f"\nB / C ratio: {results['B (Full Divergence)'] / results['C (Warp-Aligned)']:.2f}x")


if __name__ == "__main__":
    main()
