import json
import csv
from timeit import timeit

dataset = "dataset1_Python+P7.csv"
actions = []

if "json" in dataset:
    with open(f"../data/{dataset}", "r") as json_file:
        data = json.load(json_file)
        for a in data["actions"]:
            actions.append(
                {
                    "action": a["action"],
                    "cost": a["cost"],
                    "profit": a["profit"],
                }
            )
elif "csv" in dataset:
    with open(f"../data/{dataset}", "r") as file:
        data = csv.reader(file, delimiter=",")
        line_count: int = 0
        for row in data:
            if line_count == 0:
                line_count = line_count + 1
            else:
                if row[0] and float(row[1]) > 0 and row not in actions:
                    actions.append(
                        {
                            "action": row[0],
                            "cost": float(row[1]),
                            "profit": float(row[2]),
                        }
                    )
else:
    print("Dataset not found")


def knapsack(budget, cost, profit, n, actions):
    budget = int(budget * 100)
    dp = [[0 for b in range(budget + 1)] for i in range(n + 1)]

    for i in range(n + 1):
        for b in range(budget + 1):
            if i == 0 or b == 0:
                dp[i][b] = 0
            elif cost[i - 1] <= b:
                dp[i][b] = max(
                    profit[i - 1] + dp[i - 1][b - cost[i - 1]],
                    dp[i - 1][b],
                )
            else:
                dp[i][b] = dp[i - 1][b]

    result = dp[n][budget]
    total_profit = result / 100

    b = budget
    total_cost = 0
    actions_bought = []
    actions_details = []
    for i in range(n, 0, -1):
        if result <= 0:
            break
        if result == dp[i - 1][b]:
            continue
        else:
            actions_bought.append(actions[i - 1]["action"])
            actions_details.append(
                {
                    "action": actions[i - 1]["action"],
                    "cost": cost[i - 1],
                    "profit": profit[i - 1],
                }
            )
            total_cost += cost[i - 1]
            result = result - profit[i - 1]
            b = b - cost[i - 1]
    total_cost = total_cost / 100

    return {
        "total_profit": total_profit,
        "total_cost": total_cost,
        "actions_bought": actions_bought,
        "actions_details": actions_details,
    }


# main function
@timeit
def calculate_profit(actions):
    budget = 500
    actions = sorted(actions, key=lambda x: x["cost"], reverse=False)
    cost = [round(float(a["cost"]) * 100) for a in actions]
    profit = [round(float(a["profit"]) * 100) for a in actions]
    n = len(profit)
    return knapsack(budget, cost, profit, n, actions)


invests = calculate_profit(actions)
file_output = dataset.split(".")[0]
with open(f"../data/knapsack_{file_output}.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["action", "cost", "profit"])
    for i in invests["actions_details"]:
        writer.writerow([i["action"], i["cost"] / 100, i["profit"] / 100])
    writer.writerow(["total", invests["total_cost"], invests["total_profit"]])
