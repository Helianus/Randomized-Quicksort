# Randomized vs Deterministic Quicksort

A demonstration that randomized algorithms can outperform deterministic ones on adversarially constructed inputs.

## The Hard Instance

`make_hard_instance(n)` produces an array of the form:

```
[n, 1, 2, 3, ..., n-1]
```

This is a fully sorted array with **exactly one element out of place** — the maximum value is swapped to position 0. Only a single swap separates it from a perfectly sorted array.

### Why this breaks deterministic quicksort

Deterministic quicksort (pivot = first element) always picks `arr[0]` as the pivot. On this input:

- The pivot is immediately the maximum element.
- Every other element is smaller, so they all fall into the **left partition**.
- The right partition is always empty.
- This imbalance repeats at every recursive level.

Result: **n(n−1)/2 comparisons** — true O(n²) behaviour.

### Why randomized strategies are unaffected

Two randomized strategies are compared, both achieving O(n log n) expected comparisons:

- **Rand pivot** — picks a uniformly random pivot from the current sub-array at each recursive call.
- **Shuffle + Det** — randomly shuffles the entire array once upfront (Fisher-Yates), then runs deterministic quicksort normally.

Both inject the same amount of randomness, just at different points. No fixed adversarial input can force worst-case splits at every level under either strategy.

## Results

Measured comparison counts on the hard instance (randomized results averaged over 10 trials):

| n     | Det comparisons | Rand pivot (avg) | Shuffle+Det (avg) | Det/Rand | Det/Shuffle |
|------:|----------------:|-----------------:|------------------:|---------:|------------:|
|   100 |           4,950 |            662.0 |             648.1 |    7.48x |       7.64x |
|   500 |         124,750 |          4,775.4 |           4,938.7 |   26.12x |      25.26x |
| 1,000 |         499,500 |         10,848.3 |          11,236.3 |   46.04x |      44.45x |
| 2,000 |       1,999,000 |         24,859.9 |          24,922.9 |   80.41x |      80.21x |

The ratio grows with n — consistent with O(n²) vs O(n log n). Rand pivot and Shuffle+Det are statistically indistinguishable, confirming they are equivalent strategies.

## Theoretical Reference

| n     | Det ~ n(n−1)/2 | Rand/Shuffle ~ 2n·log₂(n) |
|------:|---------------:|---------------------------:|
|   100 |          4,950 |                      1,328 |
|   500 |        124,750 |                      8,966 |
| 1,000 |        499,500 |                     19,931 |
| 2,000 |      1,999,000 |                     43,863 |
| 5,000 |     12,497,500 |                    123,897 |

## Running

```bash
python quicksort.py
```

Requires Python 3.6+. No external dependencies.

## File

- [quicksort.py](quicksort.py) — implementation of all three algorithms, hard instance construction, and benchmark.
