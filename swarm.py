import pygame
import sys
from creature import Creature
from grid import Grid
import random

# Create grid and creatures
grid = Grid()
creatures = [Creature(grid) for _ in range(5)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((grid.get_window_width(), grid.get_window_height()))
grid_surface = pygame.Surface((grid.get_window_width(), grid.get_window_height()))
grid.draw(grid_surface)  # Draw the grid once onto the surface
pygame.display.set_caption("Grid World with Creatures")
clock = pygame.time.Clock()

# Simulation Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear screen
    screen.fill((255, 255, 255))

    # Draw grid
    screen.blit(grid_surface, (0, 0))  # Blit the pre-rendered grid instead of redrawing

    # Update and draw creatures
    for creature in creatures:
        creature.move()
        creature.draw(screen)
    
    # Update display
    pygame.display.flip()
    # Limits the updates per second
    clock.tick(60)