import csv
import json
from timeit import timeit

# calculate profit for each action
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
            if float(row[1]) > 0:
                actions.append(
                    {
                        "action": row[0],
                        "cost": float(row[1]),
                        "profit": float(row[2]),
                    }
                )


@timeit
def calculate_profit(actions):
    """
    A function to calculate the best investments from a list of actions within a budget constraint.

    Parameters:
    - actions (list of dict): A list of actions with keys "cost" and "profit" representing the cost and profit values respectively.

    Returns:
    - best_invests (dict): A dictionary containing the best investment actions within the budget constraint, along with total cost and total profit.
    """
    for a in actions:
        a["profit"] = a["cost"] * a["profit"] / 100

    # sort descending by profit
    actions = sorted(actions, key=lambda x: x["profit"], reverse=True)

    # sum <= 500 (from first to last)
    best_invests = {
        "actions": [],
        "total_cost": 0,
        "total_profit": 0,
    }
    for a in actions:
        if best_invests["total_cost"] + a["cost"] <= 500:
            best_invests["total_cost"] += a["cost"]
            best_invests["total_profit"] += a["profit"]
            best_invests["actions"].append(a)

    return best_invests


print(calculate_profit(actions))
