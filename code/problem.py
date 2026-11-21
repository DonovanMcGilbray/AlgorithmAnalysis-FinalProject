# loads project data, checks valid solutions, and lists available solving methods
# Input Data:
#   budget - total money available
#   n - number of projects
#   cost - cost of each project
#   benefit - benefit score of each project
#   projects - extra details for each project
# Output: a list of unique project IDs that stay within budget

import json

sense = "max"
techniques = {
    "dp": {"name": "Dynamic programming (0/1 knapsack table)", "exact": True},
    "greedy": {"name": "Greedy", "exact": False},
}

def load_instance(path, params=None):
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    projs = raw["projects"]
    return {
        "budget": raw["budget_10k"], "n": len(projs),
        "cost": [p["cost_10k"] for p in projs], "benefit": [p["benefit"] for p in projs],
        "projects": projs
    }

def validate(inst, sol, params=None):
    try:
        ids = [int(i) for i in sol]
    except (TypeError, ValueError):
        return False, None, "solution must be a list of project ids"
    if len(set(ids)) != len(ids):
        return False, None, "a project is listed twice"
    if any(i < 0 or i >= inst["n"] for i in ids):
        return False, None, "unknown project id"
    cost = sum(inst["cost"][i] for i in ids)
    if cost > inst["budget"]:
        return False, None, f"total cost {cost} exceeds budget {inst['budget']}"
    return True, sum(inst["benefit"][i] for i in ids), ""