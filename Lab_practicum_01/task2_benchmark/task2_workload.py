
import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = int(math.isqrt(n))
    for d in range(3, limit + 1, 2):
        if n % d == 0:
            return False
    return True


def count_primes_in_range(bounds: tuple[int, int]) -> int:
    lo, hi = bounds
    return sum(1 for n in range(lo, hi) if is_prime(n))
