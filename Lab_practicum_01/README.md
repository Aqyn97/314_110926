# Lab Practicum 01 - Empirical Parallel Computing

Notes to myself for running this on my MacBook Air M2. Nothing in the tables
is made up, everything gets filled in after actually running the scripts.

## Task 1 - checking what my Mac actually has

M2 is Apple Silicon so a couple of the usual Intel commands don't give
anything useful (no AVX on ARM obviously). Here's what actually works:

```bash
sysctl -n machdep.cpu.brand_string
sysctl hw.physicalcpu hw.logicalcpu
sysctl -a | grep hw.optional.arm
sysctl hw.l1dcachesize hw.l1icachesize hw.l2cachesize hw.l3cachesize
system_profiler SPHardwareDataType
```

The M2 has 8 cores total but they're not all the same (4 performance + 4
efficiency), so "physical cores" isn't the whole picture the way it is on a
normal Intel chip. Worth mentioning in Q1.1 instead of pretending it's 8
identical cores.

Also don't be surprised if `hw.l3cachesize` comes back as 0. Apple Silicon
doesn't really have a traditional L3 the way Intel does, it's a shared
system-level cache instead. That's not a broken command, that's just how
the chip is built.

For Flynn's Taxonomy: one core running a single-threaded script = SISD.
The NEON stuff doing vector ops inside a core = SIMD. macOS scheduling my
Task 2 processes across P-cores and E-cores at the same time = MIMD.

## Task 2 - the actual benchmark

```bash
cd Lab_practicum_01/task2_benchmark
python3 run_scaling.py --limit 3000000
```

3,000,000 is just a starting point, adjust it up or down depending on how
long N=1 takes. I want the single-thread run to land somewhere around
8-15 seconds so the whole sweep doesn't eat the entire lab period.

Screenshot requirement: pop open Activity Monitor's CPU history window (or
`htop` if I installed it) while this is running so it shows multiple cores
lit up, not just one.

Since the M2 only has 4 performance cores, I'm expecting the scaling curve
to bend pretty hard once N goes past 4, and get worse again once it passes
8 logical threads. That's the contention wall the lab is asking about,
should line up with the P-core/E-core split from Task 1.

Results get saved to `results.csv` in that same folder, and the script
prints T1 and T2 at the end for Task 4.

## Task 3 - race condition

```bash
cd Lab_practicum_01/task3_race
python3 race_condition.py
```

Runs 10 times unsynchronized, then does a timed locked vs unlocked
comparison. `counter.value = counter.value + 1` looks like one line but
it's actually three separate steps under the hood (read, add, write), and
Python can switch threads mid-way through that, which is where the lost
updates come from.

If every single run somehow comes back as exactly 10,000,000, that can
genuinely happen on faster chips if the threads don't get interrupted at
the wrong moment often enough. If that happens on mine I'll just write it
up honestly instead of forcing a "nicer" result, and maybe try bumping
`sys.setswitchinterval()` down to force more interruptions.

## Task 4 - Amdahl and Gustafson

```bash
cd Lab_practicum_01/task4_amdahl
python3 amdahl_calc.py --t1 <T1 from task 2> --t2 <T2 from task 2>
```

Just plug in whatever T1 and T2 actually printed from the scaling run,
copy the p, Smax, S64, and Gustafson numbers into the sheet.

## Pushing this

```bash
git add .
git commit -m "Lab Practicum 01: parallel computing benchmarks"
git push origin main
```