# code from greedy.py and dp.py

from greedy import (solve_greedy, greedy_skip, greedy_stop, greedy_two_approx, greedy_order)
from dp import solve_dp, solve_dp_value_only

TECHNIQUES = {
    "greedy": solve_greedy,
    "dp": solve_dp,
}