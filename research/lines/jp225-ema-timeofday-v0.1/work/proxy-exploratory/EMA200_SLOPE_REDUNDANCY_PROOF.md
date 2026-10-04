# Why a one-bar slow-EMA slope filter is redundant at an EMA crossover

Let:

- `F` = fast EMA
- `S` = slow EMA
- `x` = current close
- `a_f` = fast EMA alpha
- `a_s` = slow EMA alpha
- `0 < a_s < a_f < 1`

EMA recursion:

`F_t = a_f x_t + (1-a_f)F_{t-1}`

`S_t = a_s x_t + (1-a_s)S_{t-1}`

## Long crossover

A long crossover requires:

`F_{t-1} <= S_{t-1}`

and

`F_t > S_t`.

Subtracting:

`F_t - S_t = (a_f-a_s)(x_t-S_{t-1}) + (1-a_f)(F_{t-1}-S_{t-1})`.

The second term is non-positive because `F_{t-1} <= S_{t-1}`.

If `x_t <= S_{t-1}`, the first term is also non-positive, so `F_t-S_t <= 0`, contradicting the required long crossover.

Therefore:

`x_t > S_{t-1}`.

But:

`S_t-S_{t-1} = a_s(x_t-S_{t-1})`.

Hence:

`S_t > S_{t-1}`.

So every valid upward fast/slow EMA crossover already implies the slow EMA rose on that bar.

## Short crossover

The symmetric argument gives:

if `F_{t-1} >= S_{t-1}` and `F_t < S_t`, then `x_t < S_{t-1}`, therefore:

`S_t < S_{t-1}`.

So every downward fast/slow EMA crossover already implies the slow EMA fell on that bar.

## Consequence

For standard EMAs calculated from the same price series, adding:

- long only when `S_t > S_{t-1}`
- short only when `S_t < S_{t-1}`

filters **zero crossover events**.

This applies generally whenever the fast EMA has a larger alpha than the slow EMA; it is not specific to 5/200 or JP225.

A non-redundant slow-trend condition would require an additional lookback or magnitude definition, which introduces a new parameter and therefore must not be added post hoc to rescue this test.
