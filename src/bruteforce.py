import csv
import json
import itertools
from timeit import timeit

actions = []
with open("../data/actions_list.json", "r") as json_file:
    data = json.load(json_file)
    actions = data["actions"]


def bruteforce(budget, actions):
    best_combination = None
    max_profit = 0

    for r in range(1, len(actions) + 1):
        for combination in itertools.combinations(actions, r):
            total_cost = sum(item["cost"] for item in combination)
            total_profit = sum(item["profit"] for item in combination)

            if total_cost <= budget and total_profit > max_profit:
                max_profit = total_profit
                best_combination = combination

    if best_combination:
        best_combinations = [item for item in best_combination]
        return {
            "total_profit": max_profit,
            "total_cost": sum(item["cost"] for item in best_combination),
            "actions_details": best_combinations,
        }
    else:
        return {
            "total_profit": 0,
            "total_cost": 0,
            "actions_details": [],
        }


# Example usage:
@timeit
def calculate_profit(actions):
    budget = 500
    return bruteforce(budget, actions)


invests = calculate_profit(actions)
with open(f"../data/bruteforce.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["action", "cost", "profit"])
    for i in invests["actions_details"]:
        writer.writerow([i["action"], i["cost"], i["profit"]])
    writer.writerow(["total", invests["total_cost"], invests["total_profit"]])
