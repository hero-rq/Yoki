import numpy as np

# Define the parameters of the simulation
initial_bet = 1
total_days = 100
games_per_day = 10
win_probability = 0.5
#additional_bet = 25
total_bankroll = 800000000000 

def simulate_baccarat_day(initial_bet, win_probability, games_per_day):
    daily_profit = 0
    for game in range(games_per_day):
        bet = initial_bet
        total_loss = 0
        while True:
            if np.random.rand() < win_probability:  # Win
                daily_profit += bet - total_loss
                break
            else:  # Lose
                additional_bet = bet * 5 
                #additional_bet = bet + total_loss
                total_loss += bet
                bet = bet * 2 + additional_bet
                if bet > total_bankroll:  # Ensure we do not exceed the bankroll
                    print("Sorry you are bankrupted !")
                    break
    return daily_profit

# Run the simulation for the given number of days
total_profit = 0
for day in range(total_days):
    daily_profit = simulate_baccarat_day(initial_bet, win_probability, games_per_day)
    total_profit += daily_profit

total_profit = str(total_profit)
print("$" + total_profit)
