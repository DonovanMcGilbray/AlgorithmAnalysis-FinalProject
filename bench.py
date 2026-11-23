import json, statistics as st, sys, time, tracemalloc, itertools
sys.path.insert(0, "code"); sys.path.insert(0, "data")
from solutions import (solve_dp, solve_dp_value_only, greedy_skip, greedy_stop,
                       greedy_two_approx, solve_greedy)
from generate_data import generate

def mk(n, seed, style="realistic", budget=None):
    d = generate(n, seed, 0.4, style=style)
    cost = [p["cost_10k"] for p in d["projects"]]; ben = [p["benefit"] for p in d["projects"]]
    return {"budget": budget if budget else d["budget_10k"], "n": n, "cost": cost, "benefit": ben}

def val(inst, ids): return sum(inst["benefit"][i] for i in ids)
def feas(inst, ids): return sum(inst["cost"][i] for i in ids) <= inst["budget"]
def med_time(f, inst, reps=5):
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); f(inst); ts.append(time.perf_counter() - t)
    return st.median(ts)

R = {}
print("\n== DP and greedy time vs n (B = 5000) ==")
R["time_vs_n"] = []
for n in [100, 200, 400, 800, 1200, 1600, 2000]:
    inst = mk(n, 1, budget=5000); c = [0]; solve_dp(inst, c)
    r = dict(n=n, cells=c[0], dp=med_time(solve_dp, inst), greedy=med_time(solve_greedy, inst))
    R["time_vs_n"].append(r)
    print(f"n={n:5d} cells={c[0]:>9,} dp={r['dp']:.3f}s greedy={r['greedy']*1000:.3f}ms  ns/cell={r['dp']/c[0]*1e9:.0f}", flush=True)

print("\n== DP time vs B (n = 500) ==")
R["time_vs_B"] = []
base = mk(500, 1)
for B in [2000, 5000, 10000, 20000, 40000, 80000]:
    inst = dict(base, budget=B); c = [0]; solve_dp(inst, c)
    r = dict(B=B, cells=c[0], dp=med_time(solve_dp, inst))
    R["time_vs_B"].append(r)
    print(f"B={B:6d} cells={c[0]:>9,} dp={r['dp']:.3f}s  ns/cell={r['dp']/c[0]*1e9:.0f}", flush=True)

print("\n== Greedy loss % vs optimum (mean of 5 seeds): skip / stop / 2-approx ==")
R["gap"] = []
for style in ["realistic", "correlated"]:
    for n in [10, 20, 40, 100, 200, 500, 1000]:
        g = {"skip": [], "stop": [], "twoapprox": []}
        for seed in range(1, 6):
            inst = mk(n, seed, style); opt = val(inst, solve_dp(inst))
            for k, f in (("skip", greedy_skip), ("stop", greedy_stop), ("twoapprox", greedy_two_approx)):
                s = f(inst); assert feas(inst, s)
                g[k].append(100.0 * (opt - val(inst, s)) / opt)
        r = dict(style=style, n=n, **{k: st.mean(v) for k, v in g.items()}, skip_max=max(g["skip"]))
        R["gap"].append(r)
        print(f"{style:10s} n={n:5d} skip={r['skip']:.3f} (max {r['skip_max']:.3f}) stop={r['stop']:.3f} 2approx={r['twoapprox']:.3f}", flush=True)

print("\n== Operation counts ==")
R["ops"] = []
for n in [100, 1000]:
    inst = mk(n, 1); c = [0]; greedy_skip(inst, c)
    R["ops"].append(dict(n=n, greedy=c[0], dp=n * (inst["budget"] + 1)))
    print(f"n={n}: greedy items considered={c[0]}, DP cells={n * (inst['budget'] + 1):,}")

print("\n== Memory estimates (1 byte per flag) ==")
for n, B in [(1000, 21645), (2000, 43757), (5000, 100000), (10000, 200000)]:
    print(f"n={n} B={B}: cells={n*(B+1):,}  flags ~ {n*(B+1)/1e6:.0f} MB   value-only ~ {(B+1)*8/1e6:.2f} MB")

print("\n== Counter-example ==")
ce = {"budget": 100, "n": 3, "cost": [1, 100, 50], "benefit": [2, 199, 80]}
best = max((val(ce, s), s) for r in range(4) for s in itertools.combinations(range(3), r) if feas(ce, s))
print("greedy skip", val(ce, greedy_skip(ce)), "stop", val(ce, greedy_stop(ce)),
      "dp", val(ce, solve_dp(ce)), "exhaustive", best[0], "2-approx", val(ce, greedy_two_approx(ce)))
json.dump(R, open("results.json", "w"), indent=1)