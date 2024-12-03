import pygame
import random
import math
from grid import Grid

SIZE = 20
COLOR = (255, 0, 0)

class Creature:

    def __init__(self, grid):
        
        x = random.randint(0, grid.get_grid_size() - 1)
        y = random.randint(0, grid.get_grid_size() - 1)

        self.position = pygame.Vector2(x, y)  # Position as a vector
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))  # Random velocity
        self.direction = self.velocity.normalize()  # Direction vector
        self.size = SIZE  # Creature size independent of the grid
        self.world_width = grid.get_window_width()  # Width of the world
        self.world_height = grid.get_window_height()  # Height of the world
    
    
    def move(self):
        self.position += self.velocity

        # Check for collisions with borders and reverse direction
        if self.position.x - self.size < 0 or self.position.x + self.size > self.world_width:
            self.velocity.x *= -1  # Reverse x direction
            self.position.x = max(self.size, min(self.world_width - self.size, self.position.x))  # Clamp position
        
        if self.position.y - self.size < 0 or self.position.y + self.size > self.world_height:
            self.velocity.y *= -1  # Reverse y direction
            self.position.y = max(self.size, min(self.world_height - self.size, self.position.y))  # Clamp position
    

    def draw(self, screen):
        # Orientation logic for a triangle
        angle = math.atan2(self.velocity.y, self.velocity.x)  # Angle of movement in radians
        tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.size
        left = self.position + pygame.Vector2(math.cos(angle + 2 * math.pi / 3), math.sin(angle + 2 * math.pi / 3)) * (self.size / 2)
        right = self.position + pygame.Vector2(math.cos(angle - 2 * math.pi / 3), math.sin(angle - 2 * math.pi / 3)) * (self.size / 2)
        
        # Convert coordinates to integers for rendering
        points = [(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))]
        
        # Draw the triangle
        pygame.draw.polygon(screen, COLOR, points)