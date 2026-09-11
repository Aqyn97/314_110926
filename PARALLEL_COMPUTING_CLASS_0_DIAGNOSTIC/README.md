# Parallel Computing — Class 0 Diagnostic

This project contains my solutions for the Class 0 diagnostic.

It covers basic programming, algorithms, complexity, data processing, system concepts, and some problem-solving questions.

## How to run

Run:

```bash
python3 lab.py
```

The program will go through all 16 tasks and print the results in order.

## What is included

### Part A — Programming Basics

* Tracing a simple program
* Finding and fixing a bug
* Understanding nested loops

### Part B — Algorithms and Complexity

* Comparing `O(n)` and `O(n²)`
* Ranking common time complexities
* Linear search and binary search

### Part C — Data and Problem Solving

* Finding the maximum value in a large dataset
* Counting values using a dictionary
* Matrix addition and multiplication

### Part D — Systems

* CPU vs memory bottlenecks
* What happens when a program starts
* How multiple programs share the CPU

### Part E — Reasoning

* Understanding why making a computer faster doesn't always make a program twice as fast
* Finding the main bottleneck in a program
* Basic ideas from Amdahl's Law

### Final Challenge

The last task works with a large number of student marks. It calculates:

* minimum
* maximum
* average
* median
* number of marks `>= 90`
* number of marks `< 40`

Since the marks are only from `0` to `100`, a small frequency array can be used instead of storing everything for the calculations.

## Note about the large datasets

Task 7 mentions **500 million numbers** and Task 16 mentions **10 million marks**.

I use smaller datasets for the actual demo so the program doesn't take too long to run. The main algorithms and their complexity stay the same.

## Files

```text
diagnostic.py
README.md
```
