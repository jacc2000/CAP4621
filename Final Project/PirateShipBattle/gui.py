from properties import Game

import pygame
pygame.init()
pygame.font.init
pygame.display.set_caption("Pirate Ship Battle")
myfont = pygame.font.SysFont("chalkduster", 60)

# global variables
SQUARE_SIZE = 45
HORIZONTAL_MARGIN = SQUARE_SIZE * 4
VERTICAL_MARGIN = SQUARE_SIZE
HEIGHT = SQUARE_SIZE * 10 * 2 + VERTICAL_MARGIN
WIDTH = SQUARE_SIZE * 10 * 2 + HORIZONTAL_MARGIN
INDENT = 10
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_IMAGE = pygame.image.load("ocean.jpeg")
HUMAN1 = True
HUMAN2 = False

# colors
GREEN = (17, 187, 21)
GREY = (50, 50, 60)
WHITE = (255, 250, 250)
RED = (230, 27, 35)
NAVY = (20,55,80)
ORANGE = (250, 140, 20)
COLORS = {"UNKNOWN": NAVY, "MISS": WHITE, "HIT": GREEN, "SUNK": RED}

# function to draw a grid
def create_grid(player, left = 0, top = 0, search = False):
    for i in range(100):
        x = left + i % 10 * SQUARE_SIZE
        y = top + i // 10 * SQUARE_SIZE
        square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 4)
        if search:
            x += SQUARE_SIZE // 2
            y += SQUARE_SIZE // 2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x,y), radius = SQUARE_SIZE//4)

# function to draw ships onto the position grids
def create_ships(player, left = 0, top = 0):
    for ship in player.ships:
        x = left + ship.col * SQUARE_SIZE + INDENT
        y = top + ship.row * SQUARE_SIZE + INDENT
        if ship.orientation == "horizontal":
            width = ship.size * SQUARE_SIZE - 2*INDENT
            height = SQUARE_SIZE - 2*INDENT
        else:
            width = SQUARE_SIZE - 2*INDENT
            height = ship.size * SQUARE_SIZE - 2*INDENT
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, ORANGE, rectangle, border_radius = 30)

game = Game(HUMAN1, HUMAN2)

# pygame loop
animating = True
pausing = False
while animating:
    
    # track user interation
    for event in pygame.event.get():
        
        # User closes the pygame window
        if event.type == pygame.QUIT:
            animating = False
            
        # user clicks on mouse
        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
            x,y = pygame.mouse.get_pos()
            if game.player1_turn and x < SQUARE_SIZE*10 and y < SQUARE_SIZE*10:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                index = row * 10 + col
                game.move(index)
            elif not game.player1_turn and x > WIDTH - SQUARE_SIZE*10 and y > SQUARE_SIZE*10 + VERTICAL_MARGIN:
                row = (y - SQUARE_SIZE*10 - VERTICAL_MARGIN)// SQUARE_SIZE
                col = (x - SQUARE_SIZE*10 - HORIZONTAL_MARGIN) // SQUARE_SIZE
                index = row * 10 + col
                game.move(index)
            
        # user presses key on keyboard
        if event.type == pygame.KEYDOWN:
            
            # escape key to close the animation
            if event.key == pygame.K_ESCAPE:
                animating = False
            
            # space bar to pause and unpause the animation
            if event.key == pygame.K_SPACE:
                pausing = not pausing
                
            # return key to restart the game
            if event.key == pygame.K_RETURN:
                game = Game(HUMAN1, HUMAN2)

    
    # execution
    if not pausing:
        
        # draw background
        SCREEN.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the ocean background
        
        # draw search grids
        create_grid(game.player1, search = True)
        create_grid(game.player2, search = True, left = (WIDTH-HORIZONTAL_MARGIN)//2 + HORIZONTAL_MARGIN, top = (HEIGHT-VERTICAL_MARGIN)//2 + VERTICAL_MARGIN)
        
        # draw position grids
        create_grid(game.player1, top = (HEIGHT-VERTICAL_MARGIN)//2 + VERTICAL_MARGIN)
        create_grid(game.player2, left = (WIDTH-HORIZONTAL_MARGIN)//2 + HORIZONTAL_MARGIN)
        
        # draw ships onto position grids
        create_ships(game.player1, top = (HEIGHT-VERTICAL_MARGIN)//2 + VERTICAL_MARGIN)
        create_ships(game.player2, left = (WIDTH-HORIZONTAL_MARGIN)//2 + HORIZONTAL_MARGIN)
        
        # computer moves
        if not game.over and game.ai_turn:
            if game.player1_turn:
                game.random_ai()
            else:
                game.hybrid_ai()
        
        # game over message
        if game.over:
            text = "Pirate " + str(game.result) + " wins!"
            textbox = myfont.render(text, False, NAVY, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 - 240 , HEIGHT//2 - 50))
        
        # update screen
        pygame.time.wait(0)
        pygame.display.flip()
