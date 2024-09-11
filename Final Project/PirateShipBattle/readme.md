# Pirate Ship Battle

Welcome to Pirate Ship Battle, a strategic turn-based game inspired by the classic game Battleship. This implementation enhances the traditional gameplay with a pirate theme and includes both a graphical user interface and sophisticated AI opponents.

## Getting Started

These instructions will guide you through getting a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The game is developed in Python and utilizes the Pygame library for its graphical interface. To run the game, ensure you have Python and Pygame installed on your system. You can install Python from [python.org](https://python.org) and Pygame using pip:

pip install pygame

### Launching Game

To launch Pirate Ship Battle, navigate to the project directory and execute the following command in your terminal:

python3 gui.py

This command will initiate Pirate Ship Battle, where you will play as Player 1 against Player 2, which is controlled by an AI.

### Configuration Options

The game's behavior can be customized by modifying the gui.py file. Here are the settings you can change:

Players: By default, you are Player 1, and Player 2 is controlled by the AI. You can configure the game for two human players or change the AI that controls Player 2.
AI Settings: The default AI for Player 2 is hybrid_ai, designed to provide a challenging yet manageable gameplay experience. You can switch to other AI strategies, such as random_ai, greedy_ai, or monte_carlo_ai, by updating the AI function calls within gui.py.

### Automated Simulations

To automatically simulate multiple games and analyze statistics like win rates and average moves per game, use the testing.py script. Execute the following command to start simulations:

python3 testing.py

This script will run multiple instances of the game in the background, gathering data on performance across different AI configurations.