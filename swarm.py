import pygame
import sys
from creature import Creature
from grid import Grid
import random

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 600
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid World with Creatures")
clock = pygame.time.Clock()

# Create grid and creatures
grid = Grid(GRID_SIZE, CELL_SIZE)
creatures = [Creature(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(5)]

# Simulation Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear screen
    screen.fill((255, 255, 255))

    # Draw grid
    grid.draw(screen)

    # Update and draw creatures
    for creature in creatures:
        creature.move()
        creature.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)