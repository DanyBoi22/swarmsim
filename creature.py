import pygame
import random
import math
from grid import Grid

SIZE = 20 # Creature size independent of the grid
COLOR = (255, 0, 0) # Creature color as rgb 
VICINITY_RADIUS = 50 # Radius of creatures vicinity
MIN_DISTANCE = 30 # minimal distance to other creatures 
MAX_VELOCITY = 2 # maximal velocity multiplier

class Creature:

    def __init__(self, grid):
        
        self.size = SIZE
        self.vicinity_radius = VICINITY_RADIUS 
        self.min_distance = MIN_DISTANCE
        self.max_velocity = MAX_VELOCITY

        self.standart_velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * self.max_velocity  # Random standart velocity
        x = random.randint(0, grid.get_grid_size() - 1) # random starting x position
        y = random.randint(0, grid.get_grid_size() - 1) # random starting y position
        self.position = pygame.Vector2(x, y)
        self.velocity = self.standart_velocity 
        #self.direction = self.velocity.normalize()
    
        self.world_width = grid.get_window_width()  # Width of the world
        self.world_height = grid.get_window_height()  # Height of the world
        
    def move(self, creatures_list):

        cohesion_force = self.cohesion(creatures_list)
        alignment_force = self.alignment(creatures_list)
        separation_force = self.separation(creatures_list)
        
        # Combine the forces
        total_force = cohesion_force + alignment_force + separation_force
        if total_force.length() > 0:
            self.velocity += total_force
            self.velocity = self.velocity.normalize() * self.max_velocity  # Ensure the creature doesn't go too fast

        self.position += self.velocity
        self.border_check()
        
    def border_check(self):
        # Check for collisions with borders and reverse direction
        if self.position.x - self.size < 0 or self.position.x + self.size > self.world_width:
            self.velocity.x *= -1  # Reverse x direction
            self.position.x = max(self.size, min(self.world_width - self.size, self.position.x))  # Clamp position
        
        if self.position.y - self.size < 0 or self.position.y + self.size > self.world_height:
            self.velocity.y *= -1  # Reverse y direction
            self.position.y = max(self.size, min(self.world_height - self.size, self.position.y))  # Clamp position
    
    def cohesion(self, creatures_list):
        """
        Cohesion involves finding the center of mass of all nearby creatures and making the creature move towards that center. 
        The strength of this force depends on the proximity of other creatures.
        """
        center_of_mass = pygame.Vector2(0, 0)
        total_nearby = 0
        
        for other in creatures_list:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius:
                    center_of_mass += other.position
                    total_nearby += 1
        
        if total_nearby > 0:
            center_of_mass /= total_nearby
            direction = (center_of_mass - self.position).normalize()
            return direction
        return pygame.Vector2(0, 0)
    
    def alignment(self, creatures):
        """
        Alignment involves matching the velocity (or direction) of nearby creatures. 
        The force will make the creature gradually align with the average direction of other creatures within the given radius.
        """
        average_velocity = pygame.Vector2(0, 0)
        total_nearby = 0

        for other in creatures:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius:
                    average_velocity += other.velocity
                    total_nearby += 1

        if total_nearby > 0:
            average_velocity /= total_nearby
            return average_velocity.normalize()
        return pygame.Vector2(0, 0)
    
    def separation(self, creatures_list):
        """
        Separation ensures that creatures do not crowd each other. 
        If they are too close, they will move away from one another to maintain a safe distance.
        """
        separation_vector = pygame.Vector2(0, 0)
            
        for other in creatures_list:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius and dist < self.min_distance:
                    # Move away from the nearby creature
                    separation_vector += (self.position - other.position).normalize() / dist  # Inverse proportional to distance
        
        return separation_vector


    def draw(self, screen):
        # Orientation logic for a triangle
        """
         ToDo: Optimize 
        """
        angle = math.atan2(self.velocity.y, self.velocity.x)  # Angle of movement in radians
        tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.size
        left = self.position + pygame.Vector2(math.cos(angle + 2 * math.pi / 3), math.sin(angle + 2 * math.pi / 3)) * (self.size / 2)
        right = self.position + pygame.Vector2(math.cos(angle - 2 * math.pi / 3), math.sin(angle - 2 * math.pi / 3)) * (self.size / 2)
        
        # Convert coordinates to integers for rendering
        points = [(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))]
        
        # Draw the triangle
        pygame.draw.polygon(screen, COLOR, points)