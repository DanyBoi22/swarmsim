import pygame
import random
import math
from grid import Grid

SIZE = 20 # Creature size independent of the grid
COLOR = (255, 0, 0) # Creature color as rgb 
VICINITY_RADIUS = 50 # Radius of creatures vicinity
MIN_DISTANCE = 30 # minimal distance to other creatures 
MAX_VELOCITY = 2 # maximal velocity multiplier
MAX_TURN_RATE = 10 # maximal turn rate

class Creature:

    def __init__(self, grid):
        
        self.size = SIZE
        self.vicinity_radius = VICINITY_RADIUS 
        self.min_distance = MIN_DISTANCE
        self.max_velocity = MAX_VELOCITY
        self.max_turn_rate = math.radians(MAX_TURN_RATE)

        #self.standart_velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * self.max_velocity  # Random standart velocity
        
        x = random.randint(0, grid.get_grid_size() - 1) # random starting x position
        y = random.randint(0, grid.get_grid_size() - 1) # random starting y position
        self.position = pygame.Vector2(x, y)
        self.velocity = MAX_VELOCITY
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() # initiate random direction
    
        self.world_width = grid.get_window_width()  # Width of the world
        self.world_height = grid.get_window_height()  # Height of the world
        
    def move(self, creatures_list):
        
        """
        cohesion_force = self.cohesion(creatures_list)
        alignment_force = self.alignment(creatures_list)
        separation_force = self.separation(creatures_list)
        total_force = cohesion_force + alignment_force + separation_force
        """

        # Combine the forces
        desired_direction = self.direction_force(creatures_list)
        if desired_direction.length() > 0:
            desired_direction.normalize()

            # Gradually adjust the direction toward the desired direction
            self.direction = self.apply_inertia(self.direction, desired_direction)

        self.position += self.velocity * self.direction
        self.border_check()
        
    def border_check(self):
        # Check for collisions with borders and reverse direction
        if self.position.x - self.size < 0 or self.position.x + self.size > self.world_width:
            self.direction.x *= -1  # Reverse x direction
            self.position.x = max(self.size, min(self.world_width - self.size, self.position.x))  # Clamp position
        
        if self.position.y - self.size < 0 or self.position.y + self.size > self.world_height:
            self.direction.y *= -1  # Reverse y direction
            self.position.y = max(self.size, min(self.world_height - self.size, self.position.y))  # Clamp position
    
    def randomise_velocity(self):
        return 0
    
    def apply_inertia(self, current_direction, desired_direction):
        # Calculate the angle between the current and desired direction vectors
        current_angle = math.atan2(current_direction.y, current_direction.x)
        desired_angle = math.atan2(desired_direction.y, desired_direction.x)
        
        # Compute the angular difference and clamp it to the maximum turn rate
        angle_difference = desired_angle - current_angle
        angle_difference = (angle_difference + math.pi) % (2 * math.pi) - math.pi  # Normalize to [-π, π]
        
        if abs(angle_difference) > self.max_turn_rate:
            angle_difference = math.copysign(self.max_turn_rate, angle_difference)
        
        # Calculate the new angle and create a new direction vector
        new_angle = current_angle + angle_difference
        return pygame.Vector2(math.cos(new_angle), math.sin(new_angle))

    def direction_force(self, creatures_list):
        """
        The calculation of force that influences creatures direction. It consisnt of 3 parts: 
        - Cohesion involves finding the center of mass of all nearby creatures and making the creature move towards that center. 
        The strength of this force depends on the proximity of other creatures.
        - Alignment involves matching the direction (or velocity) of nearby creatures. 
        The force will make the creature gradually align with the average direction of other creatures within the given radius.
        - Separation ensures that creatures do not crowd each other. 
        If they are too close, they will move away from one another to maintain a safe distance.
        """


        center_of_mass = pygame.Vector2(0, 0)
        direction_to_center = pygame.Vector2(0, 0)
        average_direction = pygame.Vector2(0, 0)
        separation_direction = pygame.Vector2(0, 0)
        total_nearby = 0
        
        for other in creatures_list:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius:

                    total_nearby += 1

                    center_of_mass += other.position

                    average_direction += other.direction

                    if dist < self.min_distance:
                        # Move away from the nearby creature
                        separation_direction += (self.position - other.position)# / dist  # Inverse proportional to distance

        if total_nearby > 0:
            # cohesion
            center_of_mass /= total_nearby
            direction_to_center = (center_of_mass - self.position).normalize()

            # alignment
            average_direction /= total_nearby
            average_direction.normalize()

            # separation
            if(separation_direction != pygame.Vector2(0, 0)):
                separation_direction.normalize()

        return direction_to_center + average_direction + separation_direction
        

    def cohesion(self, creatures_list):
        
        center_of_mass = pygame.Vector2(0, 0)
        direction_to_center = pygame.Vector2(0, 0)
        total_nearby = 0
        
        for other in creatures_list:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius:
                    center_of_mass += other.position
                    total_nearby += 1
        
        if total_nearby > 0:
            center_of_mass /= total_nearby
            direction_to_center = (center_of_mass - self.position).normalize()
    
        return direction_to_center
    
    def alignment(self, creatures):
        average_direction = pygame.Vector2(0, 0)
        total_nearby = 0

        for other in creatures:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius:
                    average_direction += other.direction
                    total_nearby += 1

        if total_nearby > 0:
            average_direction /= total_nearby
            average_direction.normalize()
        
        return average_direction
    
    def separation(self, creatures_list):
        separation_direction = pygame.Vector2(0, 0)
            
        for other in creatures_list:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius and dist < self.min_distance:
                    # Move away from the nearby creature
                    separation_direction += (self.position - other.position).normalize()# / dist  # Inverse proportional to distance
        
        return separation_direction


    def draw(self, screen):
        # Orientation logic for a triangle
        """
         ToDo: Optimize 
        """
        angle = math.atan2(self.direction.y, self.direction.x)  # Angle of movement in radians
        tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.size
        left = self.position + pygame.Vector2(math.cos(angle + 2 * math.pi / 3), math.sin(angle + 2 * math.pi / 3)) * (self.size / 2)
        right = self.position + pygame.Vector2(math.cos(angle - 2 * math.pi / 3), math.sin(angle - 2 * math.pi / 3)) * (self.size / 2)
        
        # Convert coordinates to integers for rendering
        points = [(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))]
        
        # Draw the triangle
        pygame.draw.polygon(screen, COLOR, points)