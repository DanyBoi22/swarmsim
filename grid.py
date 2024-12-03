import pygame
import sys

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 10  # Number of rows and columns
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE  # Size of each cell

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (50, 150, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid World")
clock = pygame.time.Clock()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)  # Outline
    
    # Optional: Highlight cell under mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_col = mouse_x // CELL_SIZE
    hover_row = mouse_y // CELL_SIZE
    hover_rect = (hover_col * CELL_SIZE, hover_row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, HIGHLIGHT, hover_rect)

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit FPS