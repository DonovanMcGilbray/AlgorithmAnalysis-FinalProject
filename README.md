# P3 City Capital Budget Planner (0/1 knapsack): Group B

**Group B** techniques:

| Key | Technique | Time | Space | Optimal? |
|---|---|---|---|---|
| `greedy` | Best benefit/cost ratio first (skip variant) | Θ(n log n) | Θ(n) | No |
| `dp` | Dynamic programming (0/1 knapsack table, with traceback) | Θ(n·B) | Θ(B) values + n·B flags | Yes |

A city has a budget B and n candidate projects, each with an integer cost (units of $10,000) and a benefit score.
Each project is funded fully or not at all; the goal is the highest total benefit within budget.
Group A's techniques (brute force, meet-in-the-middle) are not part of this submission.

## Repository layout

    code/
      greedy.py        greedy (skip and stop variants, 2-approximation)
      dp.py            dynamic programming (table with traceback, value-only version)
      solutions.py     imports both and defines TECHNIQUES for the harness
      problem.py       instance loader and validator (provided)
      run_checks.py    correctness harness (provided)
    data/              datasets, manifest.json, generate_data.py
    docs/              report
    bench.py           timing, quality and memory experiments
    results.json       output of bench.py

## How to run

Correctness check (from the `code` folder):

    python run_checks.py solutions.py --only greedy,dp

Expected: `20 passed, 0 failed`. DP returns the proven optimum on all 10 datasets, greedy returns valid answers and the harness prints its gap to the optimum.

Experiments (from the repository root):

    python bench.py

## Results summary

- **DP is exact**, with time linear in n and B (about 70 ns per table cell); n = 2000, B = 43,757 takes about 10 s.
- **Greedy is nearly optimal on realistic data** (about 0.16% below the optimum at n = 100, 0.004% at n = 1000) and takes about 0.3 ms at n = 2000.
- **Greedy is weaker on correlated data** (benefit = cost + 10): 7.8% loss at n = 10, 3.7% at n = 40, 0.13% at n = 1000.
- **Greedy has no worst-case guarantee.** With B = 100 and projects (cost, benefit) = (1, 2), (100, 199), (50, 80), greedy funds 82 and the optimum is 199.
- **Recommendation:** use DP when n·B is up to about 10^8 and an exact answer matters; use greedy (plus the best-single-project check) for huge or instant cases.

`docs/report.md` contains pseudocode, complexity analysis and the full experiment tables.

## Implementation notes

- The DP builds each row from the previous row, so no project is used twice.
- One flag per cell lets the funded projects be recovered by traceback from `(n, B)`.
- `solve_dp_value_only` is a Θ(B)-memory version returning only the optimal value.
- Only the standard library is used; no knapsack solvers.