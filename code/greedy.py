# Greedy algorithm

def greedy_order(inst):
    # sorted by benefit/cost, best first
    cost, ben = inst["cost"], inst["benefit"]
    def key(i):
        if cost[i] == 0:
            return float("inf")
        return ben[i] / cost[i]
    return sorted(range(inst["n"]), key=key, reverse=True)

def greedy_skip(inst, counter=None):
    # go through the ranked list and fund whatever fits in the budget
    # skips anything that's too expensive
    cost = inst["cost"]
    left, chosen = inst["budget"], []
    for i in greedy_order(inst):
        if counter is not None:
            counter[0] += 1
        if cost[i] <= left:
            chosen.append(i)
            left -= cost[i]
    return chosen

def greedy_stop(inst, counter=None):
    # stop at the first project that doesn't fit
    cost = inst["cost"]
    left, chosen = inst["budget"], []
    for i in greedy_order(inst):
        if counter is not None:
            counter[0] += 1
        if cost[i] > left:
            break
        chosen.append(i)
        left -= cost[i]
    return chosen

def greedy_two_approx(inst):
    # picks whichever is better between greedy_skip or the single highest-value item
    g = greedy_skip(inst)
    fits = [i for i in range(inst["n"]) if inst["cost"][i] <= inst["budget"]]
    if not fits:
        return g
    best = max(fits, key=lambda i: inst["benefit"][i])
    gv = sum(inst["benefit"][i] for i in g)
    return g if gv > inst["benefit"][best] else [best]

def solve_greedy(inst):
    return greedy_skip(inst)