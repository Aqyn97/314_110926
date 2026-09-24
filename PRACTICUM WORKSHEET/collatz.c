/*
 * collatz.c - Amdahl Reality Gap lab (Collatz stopping time, OpenMP)
 *
 * Build:  gcc -O2 -fopenmp collatz.c -o collatz            (add -DCACHE_LINE=128 if your cache line is 128 B)
 *         (macOS: install gcc via Homebrew and use gcc-14; Apple clang has no OpenMP by default)
 *
 * Usage:  ./collatz header
 *         ./collatz <last4> seq
 *         ./collatz <last4> par <threads> <static|dynamic|guided> <chunk>   (chunk 0 = default)
 *         ./collatz <last4> fs_naive  <threads>     (Experiment A, Variant 1: hit_count[tid]++)
 *         ./collatz <last4> fs_padded <threads>     (Experiment A, Variant 2: 64-byte padded)
 *
 * <last4> = last 4 digits of Student ID; N = 10,000,000 + last4 * 1000
 * Each mode runs 3 times. Run 1 = cold (discard), Avg = (Run2 + Run3) / 2.
 * Output: one CSV line (see "header").
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define MOD 1000000007ULL
#define MAX_THREADS 256
#define RUNS 3
#ifndef CACHE_LINE
#define CACHE_LINE 64   /* Apple Silicon reports 128: compile with -DCACHE_LINE=128 */
#endif

static inline uint32_t collatz_steps(uint64_t n) {
    uint32_t steps = 0;
    while (n > 1) {
        if ((n & 1) == 0) n >>= 1;
        else n = 3 * n + 1;
        steps++;
    }
    return steps;
}

typedef struct { uint32_t max; uint64_t sum; uint64_t hits; } Result;

/* Experiment A data */
static volatile int hit_naive[MAX_THREADS];               /* adjacent ints share cache lines */
struct Padded { int count; char pad[CACHE_LINE - 4]; } __attribute__((aligned(CACHE_LINE)));
static struct Padded hit_padded[MAX_THREADS];             /* one cache line per thread */

static Result run_seq(long long N) {
    Result r = {0, 0, 0};
    for (long long i = 1; i <= N; i++) {
        uint32_t s = collatz_steps((uint64_t)i);
        if (s > r.max) r.max = s;
        r.sum += s;
        if (s > 100) r.hits++;
    }
    return r;
}

/* schedule chosen at runtime via omp_set_schedule() */
static Result run_par(long long N) {
    uint32_t mx = 0; uint64_t sum = 0, hits = 0;
    #pragma omp parallel for schedule(runtime) reduction(max:mx) reduction(+:sum,hits)
    for (long long i = 1; i <= N; i++) {
        uint32_t s = collatz_steps((uint64_t)i);
        if (s > mx) mx = s;
        sum += s;
        if (s > 100) hits++;
    }
    Result r = {mx, sum, hits};
    return r;
}

static Result run_fs_naive(long long N) {
    memset((void *)hit_naive, 0, sizeof hit_naive);
    #pragma omp parallel for schedule(static)
    for (long long i = 1; i <= N; i++) {
        if (collatz_steps((uint64_t)i) > 100) hit_naive[omp_get_thread_num()]++;
    }
    Result r = {0, 0, 0};
    for (int t = 0; t < MAX_THREADS; t++) r.hits += hit_naive[t];
    return r;
}

static Result run_fs_padded(long long N) {
    memset(hit_padded, 0, sizeof hit_padded);
    #pragma omp parallel for schedule(static)
    for (long long i = 1; i <= N; i++) {
        if (collatz_steps((uint64_t)i) > 100) hit_padded[omp_get_thread_num()].count++;
    }
    Result r = {0, 0, 0};
    for (int t = 0; t < MAX_THREADS; t++) r.hits += hit_padded[t].count;
    return r;
}

int main(int argc, char **argv) {
    if (argc >= 2 && strcmp(argv[1], "header") == 0) {
        puts("N,mode,threads,sched,chunk,run1_cold_s,run2_s,run3_s,avg_s,throughput_iter_per_s,max_steps,checksum,hits_gt100");
        return 0;
    }
    if (argc < 3) {
        fprintf(stderr, "usage: %s <last4> <seq|par|fs_naive|fs_padded> [threads] [sched] [chunk]\n", argv[0]);
        return 1;
    }
    long long last4 = atoll(argv[1]);
    long long N = 10000000LL + last4 * 1000LL;
    const char *mode = argv[2];
    int threads = (argc > 3) ? atoi(argv[3]) : 1;
    const char *sched = (argc > 4) ? argv[4] : "static";
    int chunk = (argc > 5) ? atoi(argv[5]) : 0;

    if (threads < 1 || threads > MAX_THREADS) { fprintf(stderr, "threads must be 1..%d\n", MAX_THREADS); return 1; }
    if (strcmp(mode, "seq") == 0) threads = 1;
    omp_set_num_threads(threads);

    if (strcmp(mode, "par") == 0) {
        omp_sched_t kind = omp_sched_static;
        if (strcmp(sched, "dynamic") == 0) kind = omp_sched_dynamic;
        else if (strcmp(sched, "guided") == 0) kind = omp_sched_guided;
        else if (strcmp(sched, "static") != 0) { fprintf(stderr, "bad schedule\n"); return 1; }
        omp_set_schedule(kind, chunk);
    }

    double t[RUNS];
    Result r = {0, 0, 0};
    for (int k = 0; k < RUNS; k++) {
        double t0 = omp_get_wtime();
        if      (strcmp(mode, "seq") == 0)       r = run_seq(N);
        else if (strcmp(mode, "par") == 0)       r = run_par(N);
        else if (strcmp(mode, "fs_naive") == 0)  r = run_fs_naive(N);
        else if (strcmp(mode, "fs_padded") == 0) r = run_fs_padded(N);
        else { fprintf(stderr, "unknown mode\n"); return 1; }
        t[k] = omp_get_wtime() - t0;
    }
    double avg = (t[1] + t[2]) / 2.0;

    printf("%lld,%s,%d,%s,%d,%.6f,%.6f,%.6f,%.6f,%.0f,%u,%llu,%llu\n",
           N, mode, threads, sched, chunk, t[0], t[1], t[2], avg, (double)N / avg,
           r.max, (unsigned long long)(r.sum % MOD), (unsigned long long)r.hits);
    return 0;
}