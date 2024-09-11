import random

class Ship:
    def __init__(self, size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation = random.choice(["horizontal", "vertical"])
        self.indexes = self.indexes_compute()
        
    def indexes_compute(self):
        start_index = self.row * 10 + self.col
        if self.orientation == "horizontal":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "vertical":
            return [start_index + i*10 for i in range(self.size)]
        
class Player:
    def __init__(self):
        self.ships = []
        self.search = ["UNKNOWN" for i in range(100)]
        self.ship_placement(sizes = [5,4,3,3,2])
        list_of_lists = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_lists for index in sublist]
    
    def ship_placement(self, sizes):
        for size in sizes:
            placed = False
            while not placed:
                
                # create a new ship
                ship = Ship(size)
                
                # check if placement is possible
                possible = True
                for i in ship.indexes:
                    
                    # indexes must be < 100
                    if i >= 100:
                        possible = False
                        break
                    
                    # ships cannot behave like the "snake" in the "snake game"
                    new_row = i // 10
                    new_col = i % 10
                    if new_row != ship.row and new_col != ship.col:
                        possible = False
                        break
                    
                    # ships cannot intersect:
                    for other_ship in self.ships:
                        if i in other_ship.indexes:
                            possible = False
                            break
                        
                # place the ship
                if possible:
                    self.ships.append(ship)
                    placed = True

    def display_ships(self):
        indexes = ["-" if i not in self.indexes else "X" for i in range(100)]
        for row in range(10):
            print(" ".join(indexes[(row-1)*10:row*10]))

class Game:
    def __init__(self, human1, human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.ai_turn = True if not self.human1 else False
        self.over = False
        self.result = None
        self.number_of_shots = 0
        self.probability_grid = [1] * 100  # Initialize with uniform probabilities

        
    def move(self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False
        
        # set miss or hit
        if i in opponent.indexes:
            player.search[i] = "HIT"
            hit = True
            
            # check if ship is sunk
            for ship in opponent.ships:
                sunk = True
                for i in ship.indexes:
                    if player.search[i] == "UNKNOWN":
                        sunk = False
                        break
                if sunk:
                    for i in ship.indexes:
                        player.search[i] = "SUNK"
            
        else:
            player.search[i] = "MISS"
            
        
        # check if game over
        game_over = True
        for i in opponent.indexes:
            if player.search[i] == "UNKNOWN":
                game_over = False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2
            
        
        
        # change the active team
        if not hit:
            self.player1_turn = not self.player1_turn
            
            # switch between human and computer turns
            if (self.human1 and not self.human2) or (not self.human1 and self.human2):
                self.ai_turn = not self.ai_turn
        
        # add to the number of shots fired
        self.number_of_shots += 1
            
    def random_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "UNKNOWN"]
        if len(unknown) > 0:
            random_index = random.choice(unknown)
            self.move(random_index)
        
    def greedy_ai(self):
        current_player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        # Collect all hits that have not resulted in sunk ships yet
        hits = [i for i, val in enumerate(current_player.search) if val == "HIT" and not self.is_part_of_sunk_ship(current_player, i)]

        if not hits:
            # If there are no hits to follow up on, use random AI as fallback
            self.random_ai()
        else:
            # Try to find adjacent cells to hit next
            for last_hit in hits:
                for delta in [-1, 1, -10, 10]:  # Check adjacent cells (left, right, above, below)
                    guess = last_hit + delta
                    if 0 <= guess < 100 and current_player.search[guess] == "UNKNOWN":  # Ensure guess is valid and untried
                        self.move(guess)
                        return
            # If no suitable adjacent cells, fall back to random AI
            self.random_ai()

    def is_part_of_sunk_ship(self, player, index):
        # Helper function to determine if a hit cell is part of a ship that's already sunk
        for ship in player.ships:
            if index in ship.indexes and all(player.search[idx] == "SUNK" for idx in ship.indexes):
                return True
        return False

    def monte_carlo_ai(self):
        current_player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        
        # Update probabilities based on current game state
        self.update_probability_grid(current_player)

        # Print the probability grid for visualization
        self.print_probability_grid()

        # Select the best move based on updated probabilities
        best_guess = self.select_best_guess(current_player)
        print("AI selecting move at index:", best_guess)
        if best_guess is not None:
            self.move(best_guess)

    def update_probability_grid(self, player):
        # Reset probabilities if needed or adjust based on new hits/misses
        self.probability_grid = [1] * 100  # Reset to base probability
        for idx, status in enumerate(player.search):
            if status == 'HIT':
                # Dynamically increase probabilities around the hit
                self.apply_hit_influence(idx)

    def apply_hit_influence(self, hit):
        # Increase probability in orthogonal directions
        directions = [-1, 1, -10, 10]  # left, right, up, down
        for direction in directions:
            next_idx = hit + direction
            if 0 <= next_idx < 100 and abs(next_idx % 10 - hit % 10) <= 1:
                self.probability_grid[next_idx] += 5  # Adjust the influence magnitude as needed

    def select_best_guess(self, player):
        # Find the highest probability untried cell
        max_prob = max((self.probability_grid[i] for i in range(100) if player.search[i] == 'UNKNOWN'), default=0)
        if max_prob == 0:
            return None  # No valid moves left, or all probabilities are zero
        best_options = [i for i in range(100) if self.probability_grid[i] == max_prob and player.search[i] == 'UNKNOWN']
        return random.choice(best_options) if best_options else None
    
    def print_probability_grid(self):
        print("Current Probability Grid:")
        for i in range(0, 100, 10):
            row = self.probability_grid[i:i+10]  # Get 10 cells at a time to form a row
            print(' '.join(f"{prob:2d}" for prob in row))  # Format each number with two digits for alignment
            
    def hybrid_ai(self):
        
        # setup
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "UNKNOWN"]
        hits = [i for i, square in enumerate(search) if square == "HIT"]
        
        # search in neighborhood of hits
        unknown_with_neighboring_hits1 = []
        unknown_with_neighboring_hits2 = []
        for u in unknown:
            if u+1 in hits or u-1 in hits or u-10 in hits or u+10 in hits:
                unknown_with_neighboring_hits1.append(u)
            if u+2 in hits or u-2 in hits or u-20 in hits or u+20 in hits:
                unknown_with_neighboring_hits2.append(u)
                
        # pick "U" square with direct and level-2 neighbor both marked as "H"
        for u in unknown:
            if u in unknown_with_neighboring_hits1 and u in unknown_with_neighboring_hits2:
                self.move(u)
                return 
        
        # pick square that has a neighbor marked as "H"
        if len(unknown_with_neighboring_hits1) > 0:
            self.move(random.choice(unknown_with_neighboring_hits1))
            return
        
        # checker board pattern
        checker_board = []
        for u in unknown:
            row = u // 10
            col = u % 10
            if (row + col) % 2 == 0:
                checker_board.append(u)
        if len(checker_board) > 0:
            self.move(random.choice(checker_board))
            return
        
        # random move
        self.random_ai()