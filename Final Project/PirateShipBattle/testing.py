from properties import Game
from matplotlib import pyplot

number_of_games = 1500
number_of_shots = []
player1_wins = 0
player2_wins = 0

# Run simulations of the game
for i in range(number_of_games):
    game = Game(human1=False, human2=False)  # Initialize the game with AI players
    while not game.over:
        if game.player1_turn:
            game.hybrid_ai()
        else:
            game.monte_carlo_ai()
            
    number_of_shots.append(game.number_of_shots)
    if game.result == 1:
        player1_wins += 1
    elif game.result == 2:
        player2_wins += 1

# Output results
print("Player 1 wins: ", player1_wins)
print("Player 2 wins: ", player2_wins)

# Prepare data for plotting the distribution of shots required to win
values = [number_of_shots.count(i) for i in range(17, 200)]

# Plotting results using Matplotlib
pyplot.bar(range(17, 200), values, color='blue')
pyplot.title('Distribution of Shots per Game')
pyplot.xlabel('Number of Shots')
pyplot.ylabel('Frequency')
pyplot.show()
