# CUDA Lab 02: Advanced Geometries & Stencils

**Student ID:** 230103342
**Allocated GPU Node:** Tesla T4
**CUDA Compute Capability:** 7.5
**Official Verification Token:** 56F526B2FA0CCDD31C4C

## Task 1: Warp Divergence Benchmark (N = 2^20, 1,000 iterations/element)

Kernel-only time, 1 warm-up launch, mean of 10 trials (transfers excluded).

| Kernel | Avg Kernel Time (ms) | Slowdown vs A |
|---|---|---|
| A (Uniform) | 3.1131 | 1.00x |
| B (Full Divergence) | 9.4687 | 3.04x |
| C (Warp-Aligned) | 4.2309 | 1.36x |

B / C ratio: 2.24x

**Analysis:** In Kernel B, even and odd threads inside every 32-thread warp take different
branches, so the hardware runs both paths one after the other for every warp. Path 2 uses a
division, which is slower than the multiply-add in Path 1, so B is about 3x slower than A. In
Kernel C the branch condition is the same for all threads in a warp (warp_id = idx // 32), so
each warp runs only one path and nothing is serialized. C is still slower than A because half
of the warps run the slower subtract-divide path, but it is 2.24x faster than B.

## Task 2: 1D Stencil (N = 100,007)
TASK 2 PASSED: MAX DELTA = 0.0

## Task 3: Grid-Stride Scaling (N = 16,777,216; 64 blocks x 256 threads = 16,384 threads)
TASK 3 PASSED: all 16,777,216 elements == 4.25

## Task 4: Sobel-X (2048 x 2048, 16x16 blocks, 128x128 grid)
TASK 4 PASSED: MAX DELTA = 0.0