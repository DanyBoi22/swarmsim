import time
import pygame.freetype  # For better text rendering

class Stats:
    def __init__(self, fps):
        self.font = pygame.freetype.SysFont("Arial", 16)
        self.fps = fps  # Frames per second
        self.start_time = 0
        self.end_time = 0
        self.loop_time = 0  # Time for the last simulation loop
        self.counter = 0
        self.average_time = 0
        self.average_time_sum = 0
    
    def start_frame(self):
        self.start_time = time.perf_counter()  # Start time of the loop

    def end_frame(self):
        # Update and display stats
        self.end_time = time.perf_counter()  # End time of the loop
        self.loop_time = (self.end_time - self.start_time) * 1000  # Convert to milliseconds
        self.counter += 1
        self.average_time_sum += self.loop_time

    
    def draw(self, screen):
        # Display stats on the screen
        if self.counter >= self.fps:
            self.average_time = self.average_time_sum / self.counter

            self.average_time_sum = 0
            self.counter = 0

        stats_text = [
                f"Frame Time Avg: {self.average_time:.2f} ms",
                f"Desired FPS: {int(self.fps)}",
                #f"Time for FPS: {(self.average_time * self.fps / 1000):.2f} s",
        ]

        for i, text in enumerate(stats_text):
            self.font.render_to(screen, (10, 10 + i * 20), text, (0, 0, 0))