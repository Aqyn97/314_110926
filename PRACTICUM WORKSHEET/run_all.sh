#!/bin/bash
# Usage: ./run_all.sh <last4> <physical_cores> <logical_threads>
# Example: ./run_all.sh 0984 8 16
# macOS:   CC=gcc-15 CACHE_LINE=128 ./run_all.sh 0984 8 8
L4=$1; PHYS=$2; LOGI=$3
[ -z "$LOGI" ] && { echo "usage: $0 <last4> <physical> <logical>"; exit 1; }
CC="${CC:-gcc}"
$CC -O2 -Wall -fopenmp -DCACHE_LINE=${CACHE_LINE:-64} collatz.c -o collatz || exit 1
OUT=results.csv
./collatz header > $OUT
./collatz $L4 seq >> $OUT
# Table 1: scaling
for k in $(echo 1 2 4 8 16 $PHYS $LOGI | tr ' ' '\n' | sort -nu); do
  [ $k -le $LOGI ] && ./collatz $L4 par $k static 0 >> $OUT
done
# Experiment A (physical thread count)
./collatz $L4 fs_naive  $PHYS >> $OUT
./collatz $L4 fs_padded $PHYS >> $OUT
# Experiment B (logical thread count)
./collatz $L4 par $LOGI static 0      >> $OUT
./collatz $L4 par $LOGI static 1000   >> $OUT
./collatz $L4 par $LOGI dynamic 100   >> $OUT
./collatz $L4 par $LOGI dynamic 10000 >> $OUT
./collatz $L4 par $LOGI guided 0      >> $OUT
echo "Done -> $OUT"