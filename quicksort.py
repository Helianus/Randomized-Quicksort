"""
Randomized vs Deterministic Quicksort
======================================
Hard instance: a sorted array with exactly one element out of place.
- Deterministic quicksort (always picks the FIRST element as pivot)
  degrades toward O(n^2) on nearly-sorted input.
- Randomized quicksort (picks a RANDOM pivot) expects O(n log n) regardless.

Metric: number of comparisons made during sorting.
"""

import random


# ---------------------------------------------------------------------------
# Comparison counter (shared mutable box so recursive calls can update it)
# ---------------------------------------------------------------------------
class Counter:
    def __init__(self):
        self.value = 0

    def inc(self, n=1):
        self.value += n


# ---------------------------------------------------------------------------
# Deterministic Quicksort  (pivot = first element)
# ---------------------------------------------------------------------------
def det_quicksort(arr, lo, hi, counter):
    if lo >= hi:
        return
    pivot_idx = det_partition(arr, lo, hi, counter)
    det_quicksort(arr, lo, pivot_idx - 1, counter)
    det_quicksort(arr, pivot_idx + 1, hi, counter)


def det_partition(arr, lo, hi, counter):
    pivot = arr[lo]          # always pick first element
    i = lo + 1
    for j in range(lo + 1, hi + 1):
        counter.inc()        # one comparison per iteration
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[lo], arr[i - 1] = arr[i - 1], arr[lo]
    return i - 1


# ---------------------------------------------------------------------------
# Randomized Quicksort  (pivot = random element in [lo, hi])
# ---------------------------------------------------------------------------
def rand_quicksort(arr, lo, hi, counter):
    if lo >= hi:
        return
    pivot_idx = rand_partition(arr, lo, hi, counter)
    rand_quicksort(arr, lo, pivot_idx - 1, counter)
    rand_quicksort(arr, pivot_idx + 1, hi, counter)


def rand_partition(arr, lo, hi, counter):
    r = random.randint(lo, hi)   # random pivot index
    arr[lo], arr[r] = arr[r], arr[lo]   # swap to front then reuse same logic
    return det_partition(arr, lo, hi, counter)


# ---------------------------------------------------------------------------
# Hard instance construction
# ---------------------------------------------------------------------------
def make_hard_instance(n):
    """
    Returns a sorted array of length n with exactly ONE element displaced:
    the largest element is placed at position 0 instead of the end.

    Example (n=8): [8, 1, 2, 3, 4, 5, 6, 7]
                      ^--- out of place

    Why this is hard for deterministic (first-element) pivot:
      - The pivot is immediately the maximum, so every other element goes to
        the LEFT partition and the RIGHT partition is empty.
      - This happens at EVERY level => O(n^2) comparisons.
    """
    arr = list(range(1, n + 1))   # [1, 2, ..., n]  fully sorted
    # Displace the max to the front (one swap = one unsorted element)
    arr[0], arr[-1] = arr[-1], arr[0]
    return arr                    # [n, 1, 2, ..., n-1]


# ---------------------------------------------------------------------------
# Shuffle + Deterministic Quicksort
# Pre-shuffle the hard instance once, then run deterministic quicksort.
# This is equivalent in expectation to randomized quicksort.
# ---------------------------------------------------------------------------
def shuffle_det_quicksort(arr, lo, hi, counter):
    """Shuffle arr[lo:hi+1] in-place, then sort deterministically."""
    # Fisher-Yates shuffle over the range [lo, hi]
    for i in range(hi, lo, -1):
        j = random.randint(lo, i)
        arr[i], arr[j] = arr[j], arr[i]
    det_quicksort(arr, lo, hi, counter)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def run_trial(n, num_rand_trials=10):
    hard = make_hard_instance(n)

    # --- Deterministic (no shuffle) ---
    arr_det = hard[:]
    c_det = Counter()
    det_quicksort(arr_det, 0, len(arr_det) - 1, c_det)

    # --- Randomized pivot ---
    rand_comps = []
    for _ in range(num_rand_trials):
        arr_rand = hard[:]
        c_rand = Counter()
        rand_quicksort(arr_rand, 0, len(arr_rand) - 1, c_rand)
        rand_comps.append(c_rand.value)
    avg_rand_comp = sum(rand_comps) / num_rand_trials

    # --- Shuffle + Deterministic ---
    shuffled_comps = []
    for _ in range(num_rand_trials):
        arr_shuffled = hard[:]
        c_shuffled = Counter()
        shuffle_det_quicksort(arr_shuffled, 0, len(arr_shuffled) - 1, c_shuffled)
        shuffled_comps.append(c_shuffled.value)
    avg_shuffled_comp = sum(shuffled_comps) / num_rand_trials

    return c_det.value, avg_rand_comp, avg_shuffled_comp


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys, math
    sys.setrecursionlimit(100_000)

    sizes = [100, 500, 1000, 2000, 5000]

    print("Hard instance: sorted array with the maximum placed at index 0")
    print("             (only ONE element is out of place)\n")
    print(f"{'n':>6} | {'Det':>12} | {'Rand (avg)':>12} | {'Shuffle+Det (avg)':>18} | {'Det/Rand':>10} | {'Det/Shuffle':>12}")
    print("-" * 85)

    for n in sizes:
        det_c, rand_c, shuffled_c = run_trial(n)
        print(f"{n:>6} | {det_c:>12,} | {rand_c:>12,.1f} | {shuffled_c:>18,.1f} | {det_c/rand_c:>10.2f}x | {det_c/shuffled_c:>12.2f}x")

    print()
    print("Conclusion: Shuffle+Det and Rand pivot both achieve O(n log n) expected.")
    print("            They are equivalent strategies — randomness in input vs pivot.\n")

    # Show the actual instance for a small n
    demo_n = 12
    demo = make_hard_instance(demo_n)
    print(f"Demo hard instance (n={demo_n}): {demo}")
    print(f"  -> Only arr[0]={demo[0]} is misplaced; rest are in order.\n")

    # Theoretical reference
    print("Theoretical complexity on this input:")
    for n in sizes:
        det_expected = n * (n - 1) / 2
        rand_expected = 2 * n * math.log(n)
        print(f"  n={n:>5}: Det ~ {det_expected:>10,.0f}  |  Rand/Shuffle ~ {rand_expected:>8,.0f}")
