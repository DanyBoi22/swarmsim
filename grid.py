import pygame

class Grid:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
    
    def draw(self, screen):
        # Draw the grid
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.cell_size
                y = row * self.cell_size
                pygame.draw.rect(screen, (200, 200, 200), (x, y, self.cell_size, self.cell_size), 1)