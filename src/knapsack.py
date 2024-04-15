import csv
from timeit import timeit

actions = []

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
                        "cost": round(float(row[1]) * 100),
                        "profit": round(float(row[2]) * 100),
                    }
                )


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
    for i in range(n, 0, -1):
        if result <= 0:
            break
        if result == dp[i - 1][b]:
            continue
        else:
            actions_bought.append(actions[i - 1]["action"])
            total_cost += cost[i - 1]
            result = result - profit[i - 1]
            b = b - cost[i - 1]
    total_cost = total_cost / 100

    return {
        "total profit": total_profit,
        "total cost": total_cost,
        "actions bought": actions_bought,
    }


# main function
@timeit
def calculate_profit(actions):
    budget = 500
    actions = sorted(actions, key=lambda x: x["cost"], reverse=False)
    cost = [a["cost"] for a in actions]
    profit = [a["profit"] for a in actions]
    n = len(profit)
    return knapsack(budget, cost, profit, n, actions)


print(calculate_profit(actions))
