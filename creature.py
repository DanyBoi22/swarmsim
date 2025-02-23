import pygame
import random
import math
from grid import Grid

SIZE = 15 # Creature size independent of the grid (in pixels)
COLOR = (0, 100, 255) # Creature color as rgb 
VICINITY_RADIUS = 100 # Radius of creatures vicinity (in pixels)
MIN_DISTANCE = 30 # minimal distance to other creatures (in pixels)
MAX_VELOCITY = 4 # maximal velocity multiplier (in pixels)
MAX_TURN_ANGLE = 2 # maximal turn rate during a single frame (in radians)  1 Rad is ca. 57 Degrees
MIN_TURN_ANGLE = 0.1 # minimal allowed turn (in radians) # 0.5 was not bad
MAX_VELOCITY_DEVIATION = 0.05 # maximal deviation to the velocity that cann occure during a single frame (in pixels per frame)

# Influence Multipliers, you can adjust them to change creatures behaviour
BORDER_INFLUENCE_MULTIPLIER = 4
COHESION_INFLUENCE_MULTIPLIER = 1
ALIGNMENT_INFLUENCE_MULTIPLIER = 1
SEPARATION_INFLUENCE_MULTIPLIER = 1.5

class Creature:

    def __init__(self, grid):
        
        self.size = SIZE
        self.vicinity_radius = VICINITY_RADIUS 
        self.min_distance = MIN_DISTANCE
        self.max_velocity = MAX_VELOCITY
        self.max_turn_angle = math.radians(MAX_TURN_ANGLE)
        self.min_turn_angle = math.radians(MIN_TURN_ANGLE)
        self.max_velocity_deviation = MAX_VELOCITY_DEVIATION
                            
        x = random.randint(0, grid.get_grid_size() - 1) # random starting x position
        y = random.randint(0, grid.get_grid_size() - 1) # random starting y position
        self.position = pygame.Vector2(x, y)
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() # initiate random direction
        self.velocity = self.max_velocity / 2

        # Buffers for the next state
        self.next_position = self.position
        self.next_direction = self.direction
        self.next_velocity = self.velocity
    
        self.world_width = grid.get_window_width()  # Width of the world
        self.world_height = grid.get_window_height()  # Height of the world

        self.previous_direction = self.direction # for analysing purposes
        
    def calculate_next_state(self, creatures_list):
        """
        Calculates the next state of the creature. It involves direction, position and velocity of the creature in the next frame
        """

        # Calculate desired direction
        creatures_influence = self.creatures_in_vicinity_influence(creatures_list, 
                                                                   cohesion_influence_multiplier=COHESION_INFLUENCE_MULTIPLIER, 
                                                                   alignment_influence_multiplier=ALIGNMENT_INFLUENCE_MULTIPLIER, 
                                                                   separation_influence_multiplier=SEPARATION_INFLUENCE_MULTIPLIER)
        border_avoidance = self.border_check(influence_multiplier=BORDER_INFLUENCE_MULTIPLIER)
        desired_direction = creatures_influence + border_avoidance
        
        # Set the desired direction as next direction
        if desired_direction.length() > 0:
            desired_direction = desired_direction.normalize()
            self.next_direction = self.align_direction(self.direction, desired_direction)
        
        # Adjust the velocity to the nearby creatures
        self.adjust_velocity(creatures_list)

        # Calculate and the the next position based on the direction and velocity
        self.next_position += self.next_direction * self.next_velocity
        
        
    def update_state(self):
        # Apply the buffered next state
        self.direction = self.next_direction
        self.position = self.next_position
        self.velocity = self.next_velocity

        self.previous_direction = self.direction # for analysing purposes

    def border_check(self, influence_multiplier=1):
        """
        Adjust the creature's direction gradually based on proximity to borders.
        The closer to a border, the larger the turning angle to avoid collisions.
        You can adjust the influence multiplier if you want the creatures to avoid the borders more or less
        """
        # Initialize a force vector to adjust direction
        border_avoidance = pygame.Vector2(0, 0) 

        # Proximity to left and right borders
        if self.position.x - self.size < self.size * 2:  # Close to the left border
            distance_to_border = max(1, self.position.x - self.size)  # Avoid division by zero
            border_avoidance.x += (self.size * 2 - distance_to_border) / self.size

        if self.position.x + self.size > self.world_width - self.size * 2:  # Close to the right border
            distance_to_border = max(1, self.world_width - (self.position.x + self.size))  # Avoid division by zero
            border_avoidance.x -= (self.size * 2 - distance_to_border) / self.size

        # Proximity to top and bottom borders
        if self.position.y - self.size < self.size * 2:  # Close to the top border
            distance_to_border = max(1, self.position.y - self.size)  # Avoid division by zero
            border_avoidance.y += (self.size * 2 - distance_to_border) / self.size

        if self.position.y + self.size > self.world_height - self.size * 2:  # Close to the bottom border
            distance_to_border = max(1, self.world_height - (self.position.y + self.size))  # Avoid division by zero
            border_avoidance.y -= (self.size * 2 - distance_to_border) / self.size

        if border_avoidance.length() > 0:
            border_avoidance = border_avoidance.normalize() * influence_multiplier
        
        return border_avoidance
    
    def align_direction(self, current_direction, desired_direction):
        """
        Calculates the angle difference between current direction and the desired direction. 
        Then checks if its within the maximum and minimum turning angles of the creature and returns the aligned direction 
        """
        #aligned_direction 

        dot = current_direction.dot(desired_direction)
        cross = current_direction.x * desired_direction.y - current_direction.y * desired_direction.x
        angle_difference = math.atan2(cross, dot)  # Signed angle difference between current and desired direction
        
        # the desired angle is too small to turn, keep the current direction
        if abs(angle_difference) < self.min_turn_angle:           
            aligned_direction = current_direction
        # the desired angle is within the turn angles, turn to desired direction
        elif abs(angle_difference) <= self.max_turn_angle:
            aligned_direction = desired_direction
        # the desired angle is too big to turn, turn to the maximum allowed angle
        else:
            max_turn = self.max_turn_angle if angle_difference > 0 else -self.max_turn_angle
            current_angle = math.atan2(current_direction.y, current_direction.x)
            new_angle = current_angle + max_turn
            aligned_direction = pygame.Vector2(math.cos(new_angle), math.sin(new_angle))

        return aligned_direction

    def creatures_in_vicinity_influence(self, creatures_list, cohesion_influence_multiplier=1, alignment_influence_multiplier=1, separation_influence_multiplier=1):
        """
        The calculation of force that influences creatures direction. It consisnt of 3 parts: 
        - Cohesion involves finding the center of mass of all nearby creatures and making the creature move towards that center. 
        The strength of this force depends on the proximity of other creatures.
        - Alignment involves matching the direction (or velocity) of nearby creatures. 
        The force will make the creature gradually align with the average direction of other creatures within the given radius.
        - Separation ensures that creatures do not crowd each other. 
        If they are too close, they will move away from one another to maintain a safe distance.

        You can adjust the influence multipliers if you want the creatures to behave different 
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
                        # Move away from the nearby creatures
                        separation_direction += (self.position - other.position) / dist  # Inverse proportional to distance

        if total_nearby > 0:
            # Cohesion
            center_of_mass /= total_nearby
            direction_to_center = (center_of_mass - self.position)
            direction_to_center = direction_to_center / self.position.distance_to(center_of_mass) # Inverse proportional to distance to the center of mass (the farther the weaker)
            #direction_to_center = direction_to_center * self.position.distance_to(center_of_mass) # Proportional to distance to the center of mass (the closer the weaker)           
            if(direction_to_center != pygame.Vector2(0, 0)):
                direction_to_center = direction_to_center.normalize()
            
            # Alignment
            average_direction /= total_nearby
            if(average_direction != pygame.Vector2(0, 0)):
                average_direction = average_direction.normalize()

            # Separation
            if(separation_direction != pygame.Vector2(0, 0)):
                separation_direction = separation_direction.normalize()

        return direction_to_center * cohesion_influence_multiplier + average_direction * alignment_influence_multiplier + separation_direction * separation_influence_multiplier
    
    def adjust_velocity(self, creatures_list):
        """
        Adjust the velocity of the creature to the average velocity of the creatures in the vicinity
        """

        average_velocity = 0
        total_nearby = 0
        
        for other in creatures_list:
            if other != self:
                dist = self.position.distance_to(other.position)
                if dist < self.vicinity_radius:
                    total_nearby += 1
                    average_velocity += other.velocity

        if total_nearby > 0:
            average_velocity /= total_nearby
            self.align_velocity(average_velocity)

        self.randomise_velocity() # create just a little bit of randomisation to make it not that boring
    
    def align_velocity(self, average_velocity, alignment_strength=0.1):
        """
        Gradually adjust the creature's velocity towards the average velocity of its neighbors.
        The adjustment happens gradually to avoid sudden changes.
        """
        if average_velocity > 0:
            desired_velocity = average_velocity
            velocity_change = desired_velocity - self.velocity

            # Apply the limit (if the magnitude exceeds the max allowed change)
            max_change = self.max_velocity * alignment_strength
            if velocity_change > max_change:
                # Scale the velocity change to the maximum allowed magnitude
                velocity_change = max_change

            self.next_velocity += velocity_change
            self.next_velocity = max(0, min(self.next_velocity, self.max_velocity))

    def randomise_velocity(self):
        # Random change in velocity multiplier: either increase or decrease slightly
        velocity_change = random.uniform(-self.max_velocity_deviation, self.max_velocity_deviation)
        self.next_velocity = self.next_velocity + velocity_change
        
        # Keep the velocity multiplier within the range [0, max_speed]
        self.next_velocity = max(0, min(self.next_velocity, self.max_velocity))

    def draw(self, screen, debug=False):
        # create the points for the shape
        points = self.create_triangle_points()
        # Draw the shape
        pygame.draw.polygon(screen, COLOR, points)

        if debug:
            self.draw_vicinity_circle(screen, (0, 0, 0))
            self.draw_direction(self.direction, screen, (255, 0, 0))
            self.draw_direction(self.previous_direction, screen, (0, 255, 0))

    def create_triangle_points(self):
        # Orientation logic for a triangle
        """
         ToDo: Optimize 
        """
        angle = math.atan2(self.direction.y, self.direction.x)  # Angle of movement in radians
        tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * self.size
        left = self.position + pygame.Vector2(math.cos(angle + 2 * math.pi / 3), math.sin(angle + 2 * math.pi / 3)) * (self.size / 2)
        right = self.position + pygame.Vector2(math.cos(angle - 2 * math.pi / 3), math.sin(angle - 2 * math.pi / 3)) * (self.size / 2)
        
        # Convert coordinates to integers for rendering
        return[(int(tip.x), int(tip.y)), (int(left.x), int(left.y)), (int(right.x), int(right.y))]
    
    def draw_vicinity_circle(self, screen, color):
        # Draw the vicinity circle
        pygame.draw.circle(
            screen,
            color,
            (int(self.position.x), int(self.position.y)),
            self.vicinity_radius,
            1  # Outline thickness
        )

    def draw_direction(self, direction, screen, color):
         # Draw the line of sight (direction vector)
        line_end = self.position + direction * (self.vicinity_radius)  # Extend line for visibility
        pygame.draw.line(
            screen,
            color,
            (int(self.position.x), int(self.position.y)),
            (int(line_end.x), int(line_end.y)),
            2  # Line thickness
        )