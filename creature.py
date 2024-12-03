import pygame
import random
import math

class Creature:

    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)  # Position as a vector
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))  # Random velocity
        self.direction = self.velocity.normalize()  # Direction vector
        self.size = 20  # Creature size independent of the grid
    
    def move(self):
        self.position += self.velocity

    def draw(self, screen):
        # Orientation logic for a triangle
        angle = math.atan2(self.velocity.y, self.velocity.x)  # Angle of movement in radians
        tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.size
        left = self.position + pygame.Vector2(math.cos(angle + 2 * math.pi / 3), math.sin(angle + 2 * math.pi / 3)) * (self.size / 2)
        right = self.position + pygame.Vector2(math.cos(angle - 2 * math.pi / 3), math.sin(angle - 2 * math.pi / 3)) * (self.size / 2)
        
        # Convert coordinates to integers for rendering
        points = [(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))]
        
        # Draw the triangle
        pygame.draw.polygon(screen, (255, 0, 0), points)