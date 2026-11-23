# draws the graphs from results.json

import json
import matplotlib.pyplot as plt

with open("results.json", encoding="utf-8") as fh:
    R = json.load(fh)

# 1. DP and greedy time against n (B = 5000)
fig, ax = plt.subplots(figsize=(6, 4))
n = [r["n"] for r in R["time_vs_n"]]
ax.plot(n, [r["dp"] for r in R["time_vs_n"]], "o-", label="DP")
ax.plot(n, [r["greedy"] for r in R["time_vs_n"]], "s-", label="Greedy")
ax.set(xlabel="n (number of projects), B = 5000", ylabel="time (s, log scale)",
       title="Running time vs n", yscale="log")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig("plot_time_vs_n.png", dpi=150); plt.close(fig)

# 2. DP time against B (n = 500)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([r["B"] for r in R["time_vs_B"]], [r["dp"] for r in R["time_vs_B"]], "o-", color="tab:green")
ax.set(xlabel="B (budget), n = 500", ylabel="DP time (s)", title="DP running time vs B")
ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig("plot_time_vs_B.png", dpi=150); plt.close(fig)

# 3. DP time against number of cells n*(B+1)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([r["cells"] / 1e6 for r in R["time_vs_n"]], [r["dp"] for r in R["time_vs_n"]], "o", label="varying n")
ax.plot([r["cells"] / 1e6 for r in R["time_vs_B"]], [r["dp"] for r in R["time_vs_B"]], "s", label="varying B")
ax.set(xlabel="table cells n(B+1) (millions)", ylabel="DP time (s)", title="DP time vs table size")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig("plot_time_vs_cells.png", dpi=150); plt.close(fig)

# 4. Greedy loss against n, realistic vs correlated
fig, ax = plt.subplots(figsize=(6, 4))
for style, marker in (("realistic", "o-"), ("correlated", "s--")):
    g = [r for r in R["gap"] if r["style"] == style]
    ax.plot([r["n"] for r in g], [r["skip"] for r in g], marker, label=style + " (skip)")
g = [r for r in R["gap"] if r["style"] == "realistic"]
ax.plot([r["n"] for r in g], [r["stop"] for r in g], "^:", label="realistic (stop)")
ax.set(xlabel="n", ylabel="loss vs optimum (%, mean of 5 seeds)", title="Greedy solution quality",
       xscale="log", yscale="log")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig("plot_greedy_loss.png", dpi=150); plt.close(fig)

print("wrote plot_time_vs_n.png, plot_time_vs_B.png, plot_time_vs_cells.png, plot_greedy_loss.png")