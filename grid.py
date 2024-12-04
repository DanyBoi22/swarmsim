import pygame

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
GRID_SIZE = 1000
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
GRID_COLOR = (0, 255, 255)#(200, 200, 200)

class Grid:
    def __init__(self):
        self.window_height = WINDOW_HEIGHT
        self.window_width = WINDOW_WIDTH
        self.grid_size = GRID_SIZE
        self.cell_size = CELL_SIZE
    
    def draw(self, screen):
        # Draw the grid
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.cell_size
                y = row * self.cell_size
                pygame.draw.rect(screen, GRID_COLOR, (x, y, self.cell_size, self.cell_size), 1)

    def get_grid_size(self):
        return self.grid_size

    def get_window_width(self):
        return self.window_width

    def get_window_height(self):
        return self.window_height

    def get_cell_size(self):
        return self.cell_size