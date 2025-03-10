"""
The problem is the classic 0-1 Knapsack, where you're given items with specific weights and values, 
and you must select a subset that maximizes total value without exceeding a given capacity. 
Here, 'i' represents the number (or index) of items considered so far, and 'w' represents 
the current weight capacity being evaluated.
"""

def knapsack(benefits, weights, capacity):
    n = len(benefits)
    
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # building dp table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + benefits[i - 1])
                #              if not included, if included 
                #              which one is big ? 
            else:
                # Current item cannot be included, so take the value without it
                dp[i][w] = dp[i - 1][w]
    
    # beautiful
    return dp[n][capacity], dp

def main():
    benefits = [60, 100, 120]   
    weights = [10, 20, 30]    
    capacity = 50             

    max_value, dp_table = knapsack(benefits, weights, capacity)
    print("Maximum value:", max_value)
    print("table", dp_table)

if __name__ == "__main__":
    main()
