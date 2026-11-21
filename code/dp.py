# Dynamic Programming

def solve_dp(inst, counter=None):
    # dynamic programming (0/1 knapsack table)
    B, n = inst["budget"], inst["n"]
    cost, ben = inst["cost"], inst["benefit"]
    F = [0] * (B + 1)
    take = []
    for i in range(n):
        c, v = cost[i], ben[i]
        if c > B:
            take.append(bytes(B + 1))
            continue
        cand = [x + v for x in F[:B + 1 - c]]
        tail_old = F[c:]
        flags = bytes(0 if a >= b else 1 for a, b in zip(tail_old, cand))
        F = F[:c] + [a if a >= b else b for a, b in zip(tail_old, cand)]
        take.append(bytes(c) + flags)
        if counter is not None:
            counter[0] += B + 1
    chosen, w = [], B
    for i in range(n - 1, -1, -1):
        if take[i][w]:
            chosen.append(i)
            w -= cost[i]
    chosen.reverse()
    return chosen

def solve_dp_value_only(inst):
    # memory version, returns only the optimal value
    B = inst["budget"]
    F = [0] * (B + 1)
    for c, v in zip(inst["cost"], inst["benefit"]):
        for w in range(B, c - 1, -1):
            t = F[w - c] + v
            if t > F[w]:
                F[w] = t
    return F[B]