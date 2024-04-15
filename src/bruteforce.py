import csv
import itertools as it
import json
from timeit import timeit

actions = []
# with open("../data/actions_list.json", "r") as json_file:
#     data = json.load(json_file)
#     actions = data["actions"]

with open("../data/dataset1_Python+P7.csv", "r") as file:
    data = csv.reader(file, delimiter=",")
    line_count: int = 0
    for row in data:
        if line_count == 0:
            line_count = line_count + 1
        else:
            actions.append(
                {
                    "action": row[0],
                    "cost": float(row[1]),
                    "profit": float(row[2]),
                }
            )


@timeit
def iterate(arr, budget):
    """
    A function that iterates through combinations of investments within a budget to find the best investment option.

    Parameters:
    - arr: a list of investment options, each represented as a dictionary with keys "cost" and "profit"
    - budget: a float representing the maximum budget available for investments

    Returns:
    - combinations: a list of all valid investment combinations
    - best_invest: a dictionary containing the best investment option with keys "actions", "cost", and "profit"
    """
    # base case
    if len(arr) == 0 or budget <= 0:
        return [], None

    # recursive case
    combinations = []
    best_invest = {
        "action": [],
        "cost": 0,
        "profit": 0,
    }
    for n in range(1, len(arr) + 1):
        for c in it.combinations(arr, n):
            c_cost = sum([a["cost"] for a in c])
            if c_cost <= budget:
                c_profit = sum([a["cost"] * a["profit"] / 100 for a in c])
                if best_invest["profit"] < c_profit or not best_invest:
                    best_invest = {
                        "actions": c,
                        "cost": c_cost,
                        "profit": c_profit,
                    }
                combinations.append(c)

    return combinations, best_invest


combinations = iterate(actions, 500)
best_invest = combinations[1]
print(best_invest)

# write combinations to csv file

# combinations_return = []
# for c in combinations:
#     combination_return = {}
#     combination_return["actions"] = [a["action"] for a in c]
#     combination_return["cost"] = [sum([a["cost"] for a in c])]
#     combination_return["return"] = sum(
#         [a["cost"] * a["return"] / 100 for a in c]
#     )
#     combinations_return.append(combination_return)

# with open("../data/iterations.csv", "w", newline="") as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["action", "cost", "return"])
#     for c in combinations_return:
#         writer.writerow(c.values())
