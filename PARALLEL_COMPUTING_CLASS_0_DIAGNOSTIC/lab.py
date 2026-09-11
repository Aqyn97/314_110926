import time
import random
from collections import Counter


# Task 1
def task1():
    print("=== Task 1: Trace the Code ===")

    x = 5
    y = 2

    print("Start:", x, y)

    x = x + y
    print("After x = x + y:", x, y)

    y = x * 2
    print("After y = x * 2:", x, y)

    x = y - x
    print("After x = y - x:", x, y)

    print("Final:", x, y)
    print()


# Task 2
def task2():
    print("=== Task 2: Find the Bug ===")

    numbers = [10, 20, 30, 40, 50]

    # Wrong version
    total = 0
    for i in range(len(numbers)):
        total = numbers[i]

    print("Wrong result:", total)
    print("The problem is that total is replaced every time.")
    print("So in the end we only get the last number.")

    # Correct version
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]

    print("Correct sum:", total)
    print()


# Task 3
def task3():
    print("=== Task 3: Nested Loops ===")

    count = 0

    for i in range(10):
        for j in range(10):
            count += 1

    print("10 x 10 loop runs:", count, "times")
    print("1000 x 1000 loop runs:", 1000 * 1000, "times")
    print("10 x 1,000,000 loop runs:", 10 * 1_000_000, "times")
    print()


# Task 4
def task4():
    print("=== Task 4: Which Is Faster? ===")

    n = 1_000_000

    # Algorithm A checks the data once
    a = n

    # Algorithm B compares every pair
    b = n * (n - 1) // 2

    print("Algorithm A: O(n)")
    print("Algorithm B: O(n^2)")
    print()

    print("For n =", f"{n:,}")
    print("A does about", f"{a:,}", "steps")
    print("B does about", f"{b:,}", "comparisons")

    print("So Algorithm A is much faster for a large n.")
    print()


# Task 5
def task5():
    print("=== Task 5: Complexity Ranking ===")

    print("From fastest to slowest growth:")
    print("1. O(1)")
    print("2. O(log n)")
    print("3. O(n)")
    print("4. O(n log n)")
    print("5. O(n^2)")
    print("6. O(2^n)")

    print("The bigger the input gets, the more important the complexity becomes.")
    print()


# Task 6
def linear_search(numbers, target):
    for i, number in enumerate(numbers):
        if number == target:
            return i

    return -1


def binary_search(numbers, target):
    left = 0
    right = len(numbers) - 1

    while left <= right:
        middle = (left + right) // 2

        if numbers[middle] == target:
            return middle

        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


def task6():
    print("=== Task 6: Searching ===")

    numbers = [3, 8, 12, 17, 24, 31, 45, 51, 63]
    target = 45

    result1 = linear_search(numbers, target)
    result2 = binary_search(numbers, target)

    print("Numbers:", numbers)
    print("Target:", target)

    print("Linear search found it at index:", result1)
    print("Binary search found it at index:", result2)

    print()
    print("Linear search: O(n)")
    print("Binary search: O(log n)")
    print("Binary search is faster, but the list must be sorted.")
    print()


# Task 7
def task7():
    print("=== Task 7: Large Dataset ===")

    # We use a small example instead of creating 500 million numbers.
    numbers = [random.randint(0, 1_000_000_000) for _ in range(1000)]

    current_max = numbers[0]

    for number in numbers:
        if number > current_max:
            current_max = number

    print("Example maximum:", current_max)
    print()
    print("For 500 million numbers, we can use the same idea.")
    print("We don't need to keep all numbers in memory.")
    print("Just keep the biggest number found so far.")
    print("Time complexity: O(n)")
    print("Extra memory: O(1)")
    print()


# Task 8
def task8():
    print("=== Task 8: Counting ===")

    letters = list("ABACBADCAB")

    counts = Counter(letters)

    print("Input:", letters)
    print("Counts:", dict(counts))

    print("A dictionary can store each letter and its count.")
    print("We can do this in one pass through the data.")
    print()


# Task 9
def task9():
    print("=== Task 9: Matrix Operations ===")

    A = [
        [1, 2],
        [3, 4]
    ]

    B = [
        [5, 6],
        [7, 8]
    ]

    # Matrix addition
    addition = []

    for i in range(2):
        row = []

        for j in range(2):
            row.append(A[i][j] + B[i][j])

        addition.append(row)

    # Matrix multiplication
    multiplication = [
        [0, 0],
        [0, 0]
    ]

    multiply_count = 0

    for i in range(2):
        for j in range(2):
            for k in range(2):
                multiplication[i][j] += A[i][k] * B[k][j]
                multiply_count += 1

    print("A + B =", addition)
    print("A x B =", multiplication)
    print("Number of multiplications:", multiply_count)

    print("For two n x n matrices, normal multiplication is O(n^3).")
    print()


# Task 10
def task10():
    print("=== Task 10: CPU vs Memory ===")

    print("A program can be slow even with a fast CPU.")
    print()

    print("1. The program may be waiting for data from RAM.")
    print("2. There may be many cache misses.")
    print("3. Other programs may also be using CPU or memory.")

    print("In this case the problem may be memory, not the CPU itself.")
    print()


# Task 11
def task11():
    print("=== Task 11: What Happens When You Run a Program? ===")

    print("When we run a program, roughly this happens:")
    print("1. The operating system starts the program.")
    print("2. The program is loaded into memory.")
    print("3. Memory for the program is prepared.")
    print("4. The CPU starts executing the instructions.")
    print("5. The program can ask the OS for things like files or memory.")
    print("6. The program prints its output.")
    print("7. When it finishes, the OS cleans up its resources.")

    print()


# Task 12
def task12():
    print("=== Task 12: Four Programs ===")

    print("Program A: uses a lot of CPU -> CPU-bound")
    print("Program B: uses a lot of memory -> memory-bound")
    print("Program C: reads a large file -> I/O-bound")
    print("Program D: waits for user input -> mostly waiting")

    print()
    print("All four programs can run concurrently.")
    print("The operating system decides how to share the CPU between them.")

    print()
    print("With one CPU core, they are not actually running at exactly")
    print("the same time. The OS switches between the programs.")

    print()


# Task 13
def task13():
    print("=== Task 13: The Slow Program ===")

    print("Suppose a program takes 10 hours.")

    print("If we make the CPU 2 times faster,")
    print("it does NOT always mean the program will take 5 hours.")

    print("Some of the time may be spent waiting for:")
    print("- disk")
    print("- network")
    print("- other resources")

    print()
    print("Example:")

    part_that_can_be_faster = 0.8
    speedup = 2

    total_speedup = 1 / (
        (1 - part_that_can_be_faster)
        + part_that_can_be_faster / speedup
    )

    new_time = 10 / total_speedup

    print("If 80% of the program becomes 2x faster:")
    print("New time:", round(new_time, 2), "hours")

    print("This is the basic idea behind Amdahl's Law.")
    print()


# Task 14
def task14():
    print("=== Task 14: Make It Faster ===")

    ideas = [
        "Use a better algorithm.",
        "Avoid doing the same work many times.",
        "Reduce unnecessary input/output.",
        "Use multiple CPU cores.",
        "Use vectorized operations when possible.",
        "Improve memory access.",
        "Use a faster language or library for slow parts.",
        "Use approximation if exact results are not required.",
        "Profile the program before changing things."
    ]

    for i, idea in enumerate(ideas, 1):
        print(i, "-", idea)

    print()


# Task 15
def task15():
    print("=== Task 15: Bottleneck Identification ===")

    times = {
        "A": 2,
        "B": 2,
        "C": 50,
        "D": 3,
        "E": 2
    }

    total = sum(times.values())

    print("Original times:", times)
    print("Total:", total, "seconds")

    # Make everything except C 10 times faster
    new_times = {}

    for name, value in times.items():
        if name == "C":
            new_times[name] = value
        else:
            new_times[name] = value / 10

    new_total = sum(new_times.values())
    speedup = total / new_total

    print("New times:", new_times)
    print("New total:", round(new_total, 2), "seconds")
    print("Overall speedup:", round(speedup, 2), "x")

    print()
    print("C is the main bottleneck because it takes 50 seconds.")
    print("Making the other parts faster does not help very much.")
    print()


# Task 16
def task16(n=1_000_000):
    print("=== Task 16: Student Marks ===")

    print("We need to find:")
    print("- minimum")
    print("- maximum")
    print("- average")
    print("- median")
    print("- number of marks >= 90")
    print("- number of marks < 40")

    print()
    print("Marks are between 0 and 100, so we can use an array")
    print("of 101 counters instead of storing everything.")

    random.seed(42)

    marks = [random.randint(0, 100) for _ in range(n)]

    counts = [0] * 101

    minimum = 101
    maximum = -1
    total = 0

    count_90 = 0
    count_40 = 0

    start = time.perf_counter()

    for mark in marks:
        counts[mark] += 1

        if mark < minimum:
            minimum = mark

        if mark > maximum:
            maximum = mark

        total += mark

        if mark >= 90:
            count_90 += 1

        if mark < 40:
            count_40 += 1

    average = total / n

    # Find median using the counts
    middle = n // 2
    current = 0
    median = 0

    for mark in range(101):
        current += counts[mark]

        if current > middle:
            median = mark
            break

    elapsed = time.perf_counter() - start

    print()
    print("Number of marks:", f"{n:,}")
    print("Minimum:", minimum)
    print("Maximum:", maximum)
    print("Average:", round(average, 2))
    print("Median:", median)
    print("Marks >= 90:", count_90)
    print("Marks < 40:", count_40)
    print("Time:", round(elapsed, 4), "seconds")

    print()
    print("The important part is that we only need one pass through")
    print("the marks. The frequency array also helps us find the median.")
    print("Time complexity: O(n)")
    print("Extra memory: O(1) because the frequency array has only 101 values.")
    print()


if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
    task11()
    task12()
    task13()
    task14()
    task15()
    task16()

