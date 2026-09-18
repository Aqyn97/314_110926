# Monte Carlo Pi - my results

Ran everything with OpenJDK 17.0.18 (Homebrew build)

## Part 1 - unsynchronized totalHits++

```
Trial 1: totalHits=12291223  pi ~= 0.983298
Trial 2: totalHits=12121099  pi ~= 0.969688
Trial 3: totalHits=13749267  pi ~= 1.099941
Trial 4: totalHits=13980202  pi ~= 1.118416
Trial 5: totalHits=13460218  pi ~= 1.076817
```

Way off from 3.14159, and honestly worse than the 1.8-2.4 range the
worksheet mentions. Makes sense though: with 4 threads all hammering
`totalHits++` at the same time, tons of increments just get lost. Each
`totalHits++` is actually read, add 1, write back, and if two threads
read the same value before either writes back, one of those increments
disappears completely. With 50 million tosses split across 4 threads
racing on one variable, losing more than half the updates isn't
surprising at all.

## Part 2 - AtomicLong fix

```
Multithreaded (AtomicLong): pi ~= 3.141286  time=942 ms
Single-threaded baseline:   pi ~= 3.141249  time=181 ms

Slowdown factor (multi/single): 5.20x
```

Pi is accurate now, but 4 threads took 5.2x longer than a single thread
doing the same total work.

## Part 3 - thread-local reduction

```
Threads | Runtime(ms) | Speedup vs T1 | Efficiency
--------------------------------------------------
      1 |         355 |          1.00x |    100.0%
      2 |         226 |          1.57x |     78.5%
      4 |          91  |          3.90x |     97.5%
      8 |          67 |          5.30x |     66.2%
     16 |          61 |          5.82x |     36.4%
     32 |          61 |          5.82x |     18.2%
```

## Questions

**1. Why didn't 16 threads run 2x faster than 8 threads?**

Because I only have 8 cores total (4 performance + 4 efficiency, no
hyperthreading), both `hw.physicalcpu` and `hw.logicalcpu` are 8 on my M2
Air. Increasing my thread count from 8 to 16 does not give me any extra
hardware resources on which to allocate the threads. Instead, it simply means
that two threads will be taking turns on each core instead of one. Exactly
what we see here – 61ms at 16 threads and 61ms at 32 threads, which are
literally identical, as there's no extra compute to unlock beyond 8. All the
extra “parallelism” beyond the number of cores available is merely the
scheduler context switching between threads that are waiting in line for a
core. This is also why the efficiency drops sharply from 66.2% at 8 threads
to 36.4%, and then to 18.2%

**2. Why was the synchronized (Part 2) version slower than one thread?**

Since each trial just performs an insignificant amount of work
(two random doubles generation and a comparison), it takes little effort.
However, each successful trial also involves the operation of the
`AtomicLong.incrementAndGet()` method that requires a bus lock to perform
compare and swap instruction. When four threads simultaneously get a hit and try
to increment this AtomicLong, they spend most of their time waiting for the bus
lock while not performing any computations because of this cache line that gets
invalidated between cores each time when it is written to. This results in the
overhead of synchronization being much greater than the work itself,
so adding extra threads to the problem made it slower (942ms vs 181ms)